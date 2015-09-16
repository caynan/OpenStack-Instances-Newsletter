import os

username = os.environ.get('OS_USERNAME')
password = os.environ.get('OS_PASSWORD')
url = os.environ.get('OS_AUTH_URL')
project = os.environ.get('OS_TENANT_NAME')

def get_nova_credentials():
   	check_variables()

	d = {}	
	d['username'] = username 
	d['api_key'] = password
	d['auth_url'] = url
	d['project_id'] = project
	return d

def get_keystone_credentials():
	check_variables()

	d = {}
    	d['username'] = username
    	d['password'] = password
    	d['auth_url'] = url
    	d['tenant_name'] = project
    	return d

def check_variables():
	if username == None or password == None or url == None or project == None:
		raise EnvironmentError("Set environment variables.")
