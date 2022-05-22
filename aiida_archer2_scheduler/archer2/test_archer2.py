import pytest
from .slurm_archer2 import Archer2SlurmScheduler, FelxibleNodeNumber
import uuid


def test_archer2_jobresources():
    """Test for the jobresources"""
    cls = FelxibleNodeNumber

    with pytest.raises(ValueError):
        cls.validate_resources()

    # Missing required field
    with pytest.raises(ValueError):
        cls.validate_resources(num_machines=1)
    with pytest.raises(ValueError):
        cls.validate_resources(num_mpiprocs_per_machine=1)
    with pytest.raises(ValueError):
        cls.validate_resources(tot_num_mpiprocs=1)

    # Wrong field name
    with pytest.raises(ValueError):
        cls.validate_resources(num_machines=2, num_mpiprocs_per_machine=8, wrong_name=16)

    # Examples of wrong information (e.g., number of machines or of nodes < 0
    with pytest.raises(ValueError):
        cls.validate_resources(num_machines=0, num_mpiprocs_per_machine=8)
    with pytest.raises(ValueError):
        cls.validate_resources(num_machines=1, num_mpiprocs_per_machine=0)
    with pytest.raises(ValueError):
        cls.validate_resources(num_machines=1, tot_num_mpiprocs=0)
    with pytest.raises(ValueError):
        cls.validate_resources(num_mpiprocs_per_machine=1, tot_num_mpiprocs=0)

    # Examples of inconsistent information
    with pytest.raises(ValueError):
        cls.validate_resources(num_mpiprocs_per_machine=8, num_machines=2, tot_num_mpiprocs=32)

    # This should work - under populate
    cls.validate_resources(num_mpiprocs_per_machine=8, num_machines=2, tot_num_mpiprocs=8, num_cores_per_mpiproc=2)
    cls.validate_resources(num_mpiprocs_per_machine=8, num_machines=2, tot_num_mpiprocs=8)

    res = cls.validate_resources(num_mpiprocs_per_machine=8, tot_num_mpiprocs=15)
    assert res.num_machines == 2

    with pytest.raises(ValueError):
        cls.validate_resources(num_mpiprocs_per_machine=8, tot_num_mpiprocs=15, num_machines=1)

    res = cls.validate_resources(
        num_mpiprocs_per_machine=8,
        tot_num_mpiprocs=15,
        num_machines=2,
        num_cores_per_mpiproc=2,
        num_cores_per_machine=16
    )
    assert res['num_cores_per_mpiproc'] == 2


def test_submit_script():
    """
    Test the creation of a simple submission script.
    """
    from aiida.schedulers.datastructures import JobTemplate
    from aiida.common.datastructures import CodeRunMode
    from aiida.schedulers.datastructures import JobTemplateCodeInfo

    scheduler = Archer2SlurmScheduler()

    job_tmpl = JobTemplate()
    job_tmpl.shebang = '#!/bin/bash'
    job_tmpl.uuid = str(uuid.uuid4())
    job_tmpl.job_resource = scheduler.create_job_resource(num_machines=1, num_mpiprocs_per_machine=1)
    job_tmpl.max_wallclock_seconds = 24 * 3600
    code_info = JobTemplateCodeInfo()
    code_info.cmdline_params = ['mpirun', '-np', '23', 'pw.x', '-npool', '1']
    code_info.stdin_name = 'aiida.in'
    job_tmpl.codes_info = [code_info]
    job_tmpl.codes_run_mode = CodeRunMode.SERIAL

    submit_script_text = scheduler.get_submit_script(job_tmpl)

    assert submit_script_text.startswith('#!/bin/bash')

    assert '#SBATCH --no-requeue' in submit_script_text
    assert '#SBATCH --time=1-00:00:00' in submit_script_text
    assert '#SBATCH --nodes=1' in submit_script_text
    assert '#SBATCH --qos=standard' in submit_script_text
    assert '#SBATCH --partition=standard' in submit_script_text

    assert "'mpirun' '-np' '23' 'pw.x' '-npool' '1' < 'aiida.in'" in submit_script_text

    job_tmpl.qos = "short"
    submit_script_text = scheduler.get_submit_script(job_tmpl)

    assert '#SBATCH --qos=short' in submit_script_text