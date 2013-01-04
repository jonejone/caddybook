from fabric.api import env, cd, run


env.hosts = ['www.caddybok.no', ]


def deploy():
    with cd('/home/jone/caddybook/project'):
        run('git pull')
        run('sudo /etc/init.d/apache2 restart')
