from fabric.api import env, task, hosts, run, put
from textwrap import dedent

script_remote_path = '/tmp'
script_local_path = '/tmp'
script_name = 'unsecure-users.sh'
full_script_path_on_server = script_remote_path + '/' + script_name
env.unsecure_users = {}

@task
def copy_script_to_server():
    put(script_local_path + '/' + script_name, full_script_path_on_server)
    run('chmod +x ' + full_script_path_on_server)

@task
def get_unsecure_users():
    env.unsecure_users[env.host] = run(full_script_path_on_server).split()

@task
@hosts('localhost')
def show_unsecure_users():
    print '\nUnsecure users per-machine:\n'
    print env.unsecure_users


def create_script():
    unsecure_users_script = dedent('''
    #!/bin/bash

    for user in $(ls /home); do
        permissions=$(stat --format=%a /home/$user);
        if [ ${permissions:2} -ge 4 ]; then
            echo $user
        fi
    done
    ''')

    fp = open(script_local_path + '/' + script_name, 'w')
    fp.write(unsecure_users_script.strip())
    fp.close()

create_script()
