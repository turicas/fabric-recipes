from fabric.api import run, task, env, sudo

env.gitosis_config = {
        'username': 'git',
        'user_description': 'Git administrator',
        'user_home': '/opt/gitosis',
        'ssh_key_path': '/opt/gitosis/.ssh/id_rsa',
        'ssh_key_type': 'rsa',
        'gitosis_url': 'git+git://eagain.net/gitosis.git',
}

def smart_sudo(*args, **kwargs):
    if 'user' in kwargs and env.user == kwargs['user'] or not 'user' in kwargs:
        run(*args, **kwargs)
    else:
        sudo(*args, **kwargs)

def gitosis_run(command):
    sudo(command % env.gitosis_config, user=env.gitosis_config['username'])

@task
def update_list_of_apt_packages():
    '''Update the list of packages in APT'''
    smart_sudo('apt-get update')

@task
def install_aptitude_if_not_installed():
    '''Install aptitude if it isn't installed'''
    if smart_sudo('which aptitude') == '':
        smart_sudo('apt-get -y install aptitude')

@task
def install_dependencies():
    '''Install dependencies needed by gitosis to run'''
    smart_sudo('aptitude -y install sudo git-core python-setuptools')
    smart_sudo('easy_install pip')
    smart_sudo('pip install virtualenv')

@task
def create_gitosis_user():
    '''Create the Unix user that gitosis will use'''
    smart_sudo('adduser --system '
               '--shell /bin/bash '
               '--gecos "%(user_description)s" '
               '--group '
               '--disabled-password '
               '--home %(user_home)s %(username)s' % env.gitosis_config)

@task
def generate_ssh_key():
    '''Generate the SSH key to gitosis-admin'''
    smart_sudo('ssh-keygen -t %(ssh_key_type)s -N "" -f %(ssh_key_path)s' % \
               env.gitosis_config, user='git')

@task
def prepare_virtualenv():
    '''Create a virtualenv to run gitosis and activate it on bash startup'''
    run('sudo -iu %(username)s virtualenv %(user_home)s/virtualenv' % \
        env.gitosis_config) #pip's bug: https://github.com/pypa/pip/issues/381
    gitosis_run('/bin/bash -c '
                '"echo source %(user_home)s/virtualenv/bin/activate >> '
                '%(user_home)s/.bashrc"')

@task
def install_gitosis():
    '''Install gitosis using pip and add the generated SSH key as admin'''
    run('sudo -iu %(username)s %(user_home)s/virtualenv/bin/pip install '
        '%(gitosis_url)s' % env.gitosis_config)
    gitosis_run('cat %(ssh_key_path)s.pub | '
                '%(user_home)s/virtualenv/bin/gitosis-init')

@task
def all():
    '''Do the whole process of installing gitosis'''
    update_list_of_apt_packages()
    install_aptitude_if_not_installed()
    install_dependencies()
    create_gitosis_user()
    generate_ssh_key()
    prepare_virtualenv()
    install_gitosis()
