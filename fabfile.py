from fabric.api import env, cd, run, local


env.hosts = ['www.caddybok.no', ]


def flake8():
    local(
        'find . -name "*.py" -print0 | xargs -0 flake8',
        capture=False)


def deploy():
    with cd('/home/jone/caddybook/project'):
        run('git pull')
        run('sudo /etc/init.d/apache2 restart')
