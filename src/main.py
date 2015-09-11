from emailx import *
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
    projects = get_projects(keystone)
    servers = nova.servers.list(search_opts={'all_tenants': 1})
    
    for server in servers:
	flavor = nova.flavors.find(id=server.flavor['id'])
	if kwargs.has_key(server.user_id):
	     kwargs[server.user_id].update({server.name: {
					'id': server.id,
					'project_id': server.tenant_id,
					'project_name': projects[server.tenant_id],
					'cpu': flavor.vcpus, 
					'ram': flavor.ram,	
					'created': server.created,
					'status': server.status}})
	else:
	     kwargs[server.user_id] = {server.name: {
				       'id': server.id,
				       'project_id': server.tenant_id,  
				       'project_name': projects[server.tenant_id],
				       'cpu': flavor.vcpus,
				       'ram': flavor.ram,
				       'created': server.created,
				       'status': server.status}}

    return kwargs

def main():
    _creds = get_keystone_credentials()
    keystone = keystoneclient.Client(**_creds)
    _creds = get_nova_credentials()
    nova = novaclient.Client(**_creds)

    users = get_users(keystone, nova)
    send_email(users)

if __name__ == '__main__':
    main()
