Fabric Recipes
==============

Just some useful recipes I wrote using Fabric.

If you don't know Fabric, please visit:
- [Fabric's website](http://fabfile.org/)
- [Fabric's repository](https://github.com/fabric/fabric)

Recipes
-------

# `install-gitosis.py`

Install gitosis on a server with only one command-line. The server should be
Debian/Ubuntu based (you can install the dependencies manually or with your
preferred package manager if not using Debian) and you need access as root or
be a sudoer. To install, use the following command:

    fab -f install-gitosis.py -H your-username@target-machine all

# `unsecure-users.py`

Print a dictionary (in which key is the machine name and value is a list
with usernames) with a list of users that have their home folder with
permission o+r.

    fab -f unsecure-users.py -H your-username@target-machine copy_script_to_server get_unsecure_users show_unsecure_users


