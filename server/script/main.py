import re
import hashlib

from emailx import *
from credentials import *
from novaclient import client as novaclient
from keystoneclient.v2_0 import client as keystoneclient

kwargs = get_keystone_credentials()
keystone = keystoneclient.Client(**kwargs)

kwargs = get_nova_credentials()
nova = novaclient.Client(**kwargs)

def get_users():
    kwargs = {}
    users = keystone.users.list()
    servers = get_servers()

    for user in users:
	try:
	    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user.email):
	       kwargs[user.username] = {'id': user.id, 'email': user.email}
        except AttributeError:
            kwargs[user.username] = {'id': user.id, 'email': ADMIN_EMAIL}
        
        if servers.has_key(user.id):
	   kwargs[user.username].update({'servers': servers[user.id]})

    return kwargs


def get_servers():
    kwargs = {}
    servers = nova.servers.list(search_opts={'all_tenants': 1})
    for server in servers:
	flavor = nova.flavors.find(id=server.flavor['id'])
	if kwargs.has_key(server.user_id):
	     kwargs[server.user_id].update({server.name: {
					'id': server.id,
                                        'hash': set_server_hash(server.id, server.user_id),
					'cpu': '%d %s' % (flavor.vcpus, 'vCPUs' if flavor.vcpus > 1 else 'vCPU'),
					'ram': '%d MB' % flavor.ram,
					'created': '%s' % server.created[:10],
					'status': server.status}})
	else:
	     kwargs[server.user_id] = {server.name: {
				       'id': server.id,
                                       'hash': set_server_hash(server.id, server.user_id),
                                       'cpu': '%d %s' % (flavor.vcpus, 'vCPUs' if flavor.vcpus > 1 else 'vCPU'),
                                       'ram': '%d MB' % flavor.ram,
                                       'created': '%s' % server.created[:10],
                                       'status': server.status}}
    
    return kwargs


def get_server_id_by_hash(server_hash):
    servers = nova.servers.list(search_opts={'all_tenants': 1})
    
    for server in servers:
       if set_server_hash(server.id, server.user_id) == server_hash:
	  return server.id
    
    raise ValueError('Instance not Found by hash input')


def set_server_hash(server_id, salf):    
    server_hash = hashlib.sha384(server_id + salf)
    return server_hash.hexdigest()


def delete_server(server_hash):
    server_id = get_server_id_by_hash(server_hash)
    nova.servers.delete(server_id)


def main():
    users = get_users()
    send_email(users)

if __name__ == '__main__':
    main()
