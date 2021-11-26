
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/pzarabadip/aiida-orca/blob/master/LICENSE)

Compatible with:

[![aiida-core](https://img.shields.io/badge/AiiDA-%3E=1.1,%3C2.0-007ec6.svg)](https://www.aiida.net/)

# aiida-archer2-scheduler
Custom [AiiDA](www.aiida.net) scheduler/transport plugins for ARCHER2.

# How does it work?
It can be used to add custom plugins under the `aiida-scheduler` entry point. So, once you have it installed, you will have extra scheduler and transport plugins in addition to ones shipped with AiiDA. When you need to configure the computer, you simply provide the entry point that is compatible with the target machine.

# Installation
Once all files are in place and entry points are defined accordingly:

```console
pip install -e .
```

# Using the plugin

Use `verdi computer setup` to setup a ARCHER2 computer node.
Choose the `archer2.ssh` plugin for transport and `archer2.slurm` for scheduler.

Once done, use the `verdi computer configure archer2.ssh <name>` to configure the transport for the computer.

The login password should be set under the `ARCHER2_PASS` environmental variable, or `ARCHER2_PASS_<USERNAME>` for per-user basis if desired.


# Security concerns ❗

At the current state, this plugin should be strictly considered as an **workaround** rather than production code. 
This is because your password will be exposed in the environmental variable. 
Despite that they are only needed when launching daemon or accessing the files interactively, the password are stored in memory in plain text and prone to leaks.
It is highly recommanded to use a random generated password specific for ARCHER2, and have it stored safely with password managers such as KeePass.

The following guide may be useful for automate setting and removing the environmental variables:


First, Make a file called archer-pass in ~/.config, containing the following line:

```bash
export ARCHER2_PASS_<USERNAME>=<your_password>
```

Then run `gpg -c archer-pass`, which will prompt you for a password used for encrypting this file. Afterwards, there will be a `archer-pass.gpg` in the same folder file. 
You can delete the original file now.

Next, add the following function to your `.bashrc`:

```bash
archer-pass () {
        eval `gpg -d ~/.config/archer-pass.gpg 2>/dev/null`
}

unset-pass () {
        unset $(env | grep ARCHER2_PASS | awk -F'=' '{print $1}')
}

```

After restarting the terminal, you can use the `archer-pass` function in the shell to add the environmental variables: `ARCHER2_PASS_<USERNAME>`. 
It will ask you to enter the password used for encryption. Once the environmental variable are in place, start/restart the AiiDA daemon so they get picked up. 
Then you can use `unset-pass` to remove them from the environmental variable.

Note that the password needs to be set to use commands using transports, such as `verdi calcjob gotocomputer`.

# Specifying resources


```python
Dict(dict={
        'resources': {
            'tot_num_mpiprocs': cores, # Total number of MPI processes
            'num_machines': nm,  # Number of nodes to be used
            'num_mpiprocs_per_machine': num_mpi_per_machine,  # Number of mpi processes per machine - useful if underpopulating is needed
        },
        'max_wallclock_seconds': int(3600 * hours),
        'import_sys_environment': False,
        'mpirun_extra_params': ["--distribution=block:block", "--hint=nomultithread"],
        'account': '<budget_code>',
        'queue_name': '<partition_name>',
    }
```

# Changelog

## 2.0.0

- Updated the authentication order to support the ARCHER2 full system. 
- Updated entrypoint name prefixes to comply with the new aiida-core convention. Old entrypoint names remain for now to ensure backward compatibility.   

## 1.2.0

Allow per-user based password settings. 
The password should be put into `ARCHER2_PASS_<USERNAME>` where `<USERNAME>` is your username in upper case.

## 1.1.0

Added specialised scheduler for ARCHER2

# Contribution
You may kindly open and PR and add your collection to the package so it can contain all possible combinations and plugins to be used by others as well.

# Contact
zhubonan@outlook.com
