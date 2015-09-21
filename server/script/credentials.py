import json
import os
import subprocess

password = os.environ.get('OS_PASSWORD')
project = os.environ.get('OS_TENANT_NAME')
url = os.environ.get('OS_AUTH_URL')
username = os.environ.get('OS_USERNAME')

def get_nova_credentials():
    set_environments()
    args = {}	
    args['username'] = username 
    args['api_key'] = password
    args['auth_url'] = url
    args['project_id'] = project
    return args


def get_keystone_credentials():
    set_environments()
    args = {}
    args['username'] = username
    args['password'] = password
    args['auth_url'] = url
    args['tenant_name'] = project
    return args


def set_environments():
    """ Set environment variables automatically. """
    global password
    global project
    global username
    global url

    if password is None or project is None or username is None or url is None:
        os.chdir(os.path.dirname(__file__))
	
	source = 'source ../openrc.sh'
        dump = '/usr/bin/python -c "import os, json; print json.dumps(dict(os.environ))"'
        popen = subprocess.Popen(['/bin/bash', '-c', '%s && %s' % (source, dump)], stdout=subprocess.PIPE) 
        env = json.loads(popen.stdout.read())
        os.environ = env	

    password = os.environ.get('OS_PASSWORD')
    project = os.environ.get('OS_TENANT_NAME')
    url = os.environ.get('OS_AUTH_URL')
    username = os.environ.get('OS_USERNAME')
