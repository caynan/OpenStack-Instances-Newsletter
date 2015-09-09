import os
import smtplib

from credentials import *
from novaclient.v2 import client as novaclient
from keystoneclient.v2_0 import client as keystoneclient

def get_users(keystone, nova):
    kwargs = {}
    users = keystone.users.list()
    servers = get_servers(keystone, nova)    
	
    for user in users:
	try:
	    kwargs[user.username] = {'id': user.id, 'email': user.email}
	    if servers.has_key(user.id):
	       kwargs[user.username].update({'servers': servers[user.id]})
	except AttributeError:
	    continue

    return kwargs


def get_projects(keystone):
    kwargs = {}
    projects = keystone.tenants.list()

    for project in projects:
	kwargs[project.id] = project.name

    return kwargs

def get_servers(keystone, nova):
    kwargs = {}
    import pdb; pdb.set_trace();
    flavors = nova.flavors.list()
    projects = get_projects(keystone)
    servers = nova.servers.list(search_opts={'all_tenants': 1})
    
    for server in servers:
	flavor = flavors[int(server.flavor['id']) - 1]
	if kwargs.has_key(server.user_id):
	     kwargs[server.user_id].update({server.name: {
					'id': server.id,
					'project': projects[server.tenant_id],
					'cpu': flavor.vcpu 
					'ram': flavor.ram	
					'created': server.created,
					'status': server.status}})
	else:
	     kwargs[server.user_id] = {server.name: {
				       'id': server.id,  
				       'project': projects[server.tenant_id],
				       'cpu': flavor.vcpus
				       'ram': flavor.ram
				       'created': server.created,
				       'status': server.status}}

    return kwargs


def send_email(users):
    email = 'diegoado@gmail.com'
    password = raw_input()
    
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(email, password)
    
    for user in sorted(users):
	if not user.has_key('servers'):
	   continue

	servers = user['servers']
	messenger = get_messenger(servers)
    	smtp.sendmail(email, user['email'], messenger)
   
    smtp.quit()


def main():
    auth_url = os.environ.get("OS_AUTH_URL")
    password = os.environ.get("OS_PASSWORD")
    tenant = os.environ.get('OS_TENANT_NAME')
    username = os.environ.get("OS_USERNAME")
    if auth_url is None or username is None or password is None or tenant is None:
       print ("need to set env variables")
       return

    keystone = keystoneclient.Client(auth_url=auth_url, 
				     password=password, 
				     tenant_name=tenant, 
				     username=username)
    nova = novaclient.Client(api_key=password,
			     auth_url=auth_url,
			     project_id=tenant,
			     username=username)
	
    users =  get_users(keystone, nova)
    #send_email(users)

if __name__ == '__main__':
   main()
