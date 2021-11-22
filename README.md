
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/pzarabadip/aiida-orca/blob/master/LICENSE)

Compatible with:

[![aiida-core](https://img.shields.io/badge/AiiDA-%3E=1.1,%3C2.0-007ec6.svg?logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACMAAAAhCAYAAABTERJSAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAFhgAABYYBG6Yz4AAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUbSURBVFiFzZhrbFRVEMd%2Fc%2B5uu6UUbIFC%2FUAUVEQCLbQJBIiBDyiImJiIhmohYNCkqJAQxASLF8tDgYRHBLXRhIcKNtFEhVDgAxBJqgmVh4JEKg3EIn2QYqBlt917xg%2BFss%2ByaDHOtzsz5z%2B%2FuZl7ztmF%2F5HJvxVQN6cPYX8%2FPLnOmsvNAvqfwuib%2FbNIk9cQeQnLcKRL5xLIV%2Fic9eJeunjPYbRs4FjQSpTB3aS1IpRKeeOOewajy%2FKKEO8Q0DuVdKy8IqsbPulxGHUfCBBu%2BwUYGuFuBTK7wQnht6PEbf4tlRomVRjCbXNjQEB0AyrFQOL5ENIJm7dTLZE6DPJCnEtFZVXDLny%2B4Sjv0PmmYu1ZdUek9RiMgoDmJ8V0L7XJqsZ3UW8YsBOwEeHeeFce7jEYXBy0m9m4BbXqSj2%2Bxnkg26MCVrN6DEZcwggtd8pTFx%2Fh3B9B50YLaFOPwXQKUt0tBLegtSomfBlfY13PwijbEnhztGzgJsK5h9W9qeWwBqjvyhB2iBs1Qz0AU974DciRGO8CVN8AJhAeMAdA3KbrKEtvxhsI%2B9emWiJlGBEU680Cfk%2BSsVqXZvcFYGXjF8ABVJ%2BTNfVXehyms1zzn1gmIOxLEB6E31%2FWBe5rnCarmo7elf7dJEeaLh80GasliI5F6Q9cAz1GY1OJVNDxTzQTw7iY%2FHEZRQY7xqJ9RU2LFe%2FYqakdP911ha0XhjjiTVAkDwgatWfCGeYocx8M3glG8g8EXhSrLrHnEFJ5Ymow%2FkhIYv6ttYUW1iFmEqqxdVoUs9FmsDYSqmtmJh3Cl1%2BVtl2s7owDUdocR5bceiyoSivGTT5vzpbzL1uoBpmcAAQgW7ArnKD9ng9rc%2BNgrobSNwpSkkhcRN%2BvmXLjIsDovYHHEfmsYFygPAnIDEQrQPzJYCOaLHLUfIt7Oq0LJn9fxkSgNCb1qEIQ5UKgT%2Fs6gJmVOOroJhQBXVqw118QtWLdyUxEP45sUpSzqP7RDdFYMyB9UReMiF1MzPwoUqHt8hjGFFeP5wZAbZ%2F0%2BcAtAAcji6LeSq%2FMYiAvSsdw3GtrfVSVFUBbIhwRWYR7yOcr%2FBi%2FB1MSJZ16JlgH1AGM3EO2QnmMyrSbTSiACgFBv4yCUapZkt9qwWVL7aeOyHvArJjm8%2Fz9BhdI4XcZgz2%2FvRALosjsk1ODOyMcJn9%2FYI6IrkS5vxMGdUwou2YKfyVqJpn5t9aNs3gbQMbdbkxnGdsr4bTHm2AxWo9yNZK4PXR3uzhAh%2BM0AZejnCrGdy0UvJxl0oMKgWSLR%2B1LH2aE9ViejiFs%2BXn6bTjng3MlIhJ1I1TkuLdg6OcAbD7Xx%2Bc3y9TrWAiSHqVkbZ2v9ilCo6s4AjwZCzFyD9mOL305nV9aonvsQeT2L0gVk4OwOJqXXVRW7naaxswDKVdlYLyMXAnntteYmws2xcVVZzq%2BtHPAooQggmJkc6TLSusOiL4RKgwzzYU1iFQgiUBA1H7E8yPau%2BZl9P7AblVNebtHqTgxLfRqrNvZWjsHZFuqMqKcDWdlFjF7UGvX8Jn24DyEAykJwNcdg0OvJ4p5pQ9tV6SMlP4A0PNh8aYze1ArROyUNTNouy8tNF3Rt0CSXb6bRFl4%2FIfQzNMjaE9WwpYOWQnOdEF%2BTdJNO0iFh7%2BI0kfORzQZb6P2kymS9oTxzBiM9rUqLWr1WE5G6ODhycQd%2FUnNVeMbcH68hYkGycNoUNWc8fxaxfwhDbHpfwM5oeTY7rUX8QAAAABJRU5ErkJggg%3D%3D)](https://www.aiida.net/)

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

The login password should be set under the `ARCHER2_PASS` enviromental variable, or `ARCHER2_PASS_<USERNAME>` for per-user basis if desired.


# Security concerns ❗

You password will be exposed in the environmental variable. However, they are only needed when launching daemon or accessing the files interactively.
In the former case, once the daemon has started, one can safely unset the environmental variables.
It is highly recommanded to use a random generated password specific for ARCHER2, and have it stored safetly with password managers such as KeePass.

The following guide may be useful for automating this process:


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
