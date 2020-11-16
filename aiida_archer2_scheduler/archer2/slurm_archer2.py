"""
Scheduler module for ARCHER2
"""
from math import ceil
from aiida.schedulers.plugins.slurm import SlurmScheduler, NodeNumberJobResource
from aiida.common.extendeddicts import AttributeDict


class FelxibleNodeNumber(NodeNumberJobResource):
    """A more fexlible node number JobResources"""

    @classmethod
    def validate_resources(cls, **kwargs):
        """Validate the resources against the job resource class of this scheduler.

        :param kwargs: dictionary of values to define the job resources
        :return: attribute dictionary with the parsed parameters populated
        :raises ValueError: if the resources are invalid or incomplete
        """
        resources = AttributeDict()

        def is_greater_equal_one(parameter):
            value = getattr(resources, parameter, None)
            if value is not None and value < 1:
                raise ValueError('`{}` must be greater than or equal to one.'.format(parameter))

        # Validate that all fields are valid integers if they are specified, otherwise initialize them to `None`
        for parameter in list(cls._default_fields) + ['tot_num_mpiprocs']:
            value = kwargs.pop(parameter, None)
            if value is None:
                setattr(resources, parameter, None)
            else:
                try:
                    setattr(resources, parameter, int(value))
                except ValueError:
                    raise ValueError('`{}` must be an integer when specified'.format(parameter))

        if kwargs:
            raise ValueError('these parameters were not recognized: {}'.format(', '.join(list(kwargs.keys()))))

        # At least two of the following parameters need to be defined as non-zero
        if [resources.num_machines, resources.num_mpiprocs_per_machine, resources.tot_num_mpiprocs].count(None) > 1:
            raise ValueError(
                'At least two among `num_machines`, `num_mpiprocs_per_machine` or `tot_num_mpiprocs` must be specified.'
            )

        for parameter in ['num_machines', 'num_mpiprocs_per_machine']:
            is_greater_equal_one(parameter)

        # Here we now that at least two of the three required variables are defined and greater equal than one.
        # Make sure we get enough tasks
        if resources.num_machines is None:
            resources.num_machines = ceil(resources.tot_num_mpiprocs / resources.num_mpiprocs_per_machine)
        # Case when one just specify the total number of mpiprocs and the number of machines
        # assuming full utilisation
        elif resources.num_mpiprocs_per_machine is None:
            if resources.tot_num_mpiprocs % resources.num_machines != 0:
                raise ValueError(
                    "`tot_num_mpiprocs` must a multiple of num machines if `num_mpiprocs_per_machine` is not specified!"
                )
            resources.num_mpiprocs_per_machine = resources.tot_num_mpiprocs // resources.num_machines
        # Implicity specification, again assum full utilisation
        elif resources.tot_num_mpiprocs is None:
            resources.tot_num_mpiprocs = resources.num_mpiprocs_per_machine * resources.num_machines

        # Here is there difference from the original SLURM scheduler - we allow under ultilisation
        # Eg. request 256 tasks, each take 2 cpus but only use 239 tasks becuase the program prefer certain
        # multiple
        if resources.tot_num_mpiprocs >= resources.num_mpiprocs_per_machine * resources.num_machines:
            raise ValueError('`tot_num_mpiprocs` is larger than `num_mpiprocs_per_machine * num_machines`.')

        is_greater_equal_one('num_mpiprocs_per_machine')
        is_greater_equal_one('num_machines')

        return resources


class Archer2SlurmJobResource(FelxibleNodeNumber):
    """JobResources for ARCHER2 allow more flexible settings"""

    @classmethod
    def validate_resources(cls, **kwargs):
        """Validate the resources against the job resource class of this scheduler.

        This extends the base class validator to check that the `num_cores_per_machine` are a multiple of
        `num_cores_per_mpiproc` and/or `num_mpiprocs_per_machine`.

        :param kwargs: dictionary of values to define the job resources
        :return: attribute dictionary with the parsed parameters populated
        :raises ValueError: if the resources are invalid or incomplete
        """
        resources = super().validate_resources(**kwargs)

        if resources.num_cores_per_machine is not None and resources.num_cores_per_mpiproc is not None:
            if resources.num_cores_per_machine != resources.num_cores_per_mpiproc * resources.num_mpiprocs_per_machine:
                raise ValueError(
                    '`num_cores_per_machine` must be equal to `num_cores_per_mpiproc * num_mpiprocs_per_machine` and in'
                    ' particular it should be a multiple of `num_cores_per_mpiproc` and/or `num_mpiprocs_per_machine`'
                )

        elif resources.num_cores_per_machine is not None:
            if resources.num_cores_per_machine < 1:
                raise ValueError('num_cores_per_machine must be greater than or equal to one.')

            # In this plugin we never used num_cores_per_machine so if it is not defined it is OK.
            if resources.num_cores_per_machine % resources.num_mpiprocs_per_machine != 0:
                raise ValueError(
                    '`num_cores_per_machine` must be equal to `num_cores_per_mpiproc * num_mpiprocs_per_machine` and in'
                    ' particular it should be a multiple of `num_cores_per_mpiproc` and/or `num_mpiprocs_per_machine`'
                )
            resources.num_cores_per_mpiproc = int(resources.num_cores_per_machine / resources.num_mpiprocs_per_machine)

        return resources


class Archer2SlurmScheduler(SlurmScheduler):
    """
    Special scheduler for ARCHER2

    Use more flexible job resources to allow underpopulating nodes
    """
    _job_resource_class = Archer2SlurmJobResource
