import os
import re

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import sed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

f = open('secrets/inventory')
text = f.read()

env.hosts= list(re.search(".*ansible_ssh_host=(.+?)\s", text).groups())
env.user = 'deploy'
env.key_filename = './secrets/unitime-deploy-user'


def bootstrap():
    run('mkdir -p /srv/unitime/current')
    run('mkdir -p /srv/unitime/backups')
    run('mkdir -p /srv/unitime/repo')
    run('mkdir -p /srv/unitime/tmp')

    put('secrets', '/srv/unitime/')

    with cd('/srv/unitime/repo'):
        run('git clone https://github.com/Kodkollektivet/unitime-api.git .')
        run('git checkout celery-docker')

    with cd('/srv/unitime'):
        run('virtualenv --python=/usr/bin/python3 venv')
        run('venv/bin/pip install -r repo/requirements.txt')

    with cd('/srv/unitime'):
        run('cp -rf repo/* current')
        run('cp -f secrets/production.py current/settings/production.py')
        run('cp -f secrets/production.json current/settings/production.json')

    with cd('/srv/unitime/current'):
        run('find . -type f -exec sed -i.bak "s/settings.settings/settings.production/g" {} \;')

    with cd('/srv/unitime/current'):
        run('../venv/bin/python manage.py makemigrations')
        run('../venv/bin/python manage.py migrate')

    run('sudo /bin/systemctl enable unitime-celery.service')
    run('sudo /bin/systemctl enable unitime.service')
    run('sudo /bin/systemctl restart unitime-celery.service')
    run('sudo /bin/systemctl restart unitime.service')
