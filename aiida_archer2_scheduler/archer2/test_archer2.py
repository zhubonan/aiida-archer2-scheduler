import pytest
from .slurm_archer2 import FelxibleNodeNumber


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