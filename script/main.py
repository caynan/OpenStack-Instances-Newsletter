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
    projects = get_projects(keystone)
    servers = nova.servers.list(search_opts={'all_tenants': 1})
    
    for server in servers:
	flavor = nova.flavors.find(id=server.flavor['id'])
	if kwargs.has_key(server.user_id):
	     kwargs[server.user_id].update({server.name: {
					'id': server.id,
					'project': projects[server.tenant_id],
					'cpu': flavor.vcpus, 
					'ram': flavor.ram,	
					'created': server.created,
					'status': server.status}})
	else:
	     kwargs[server.user_id] = {server.name: {
				       'id': server.id,  
				       'project': projects[server.tenant_id],
				       'cpu': flavor.vcpus,
				       'ram': flavor.ram,
				       'created': server.created,
				       'status': server.status}}

    return kwargs


def send_email(users):
    email = 'your_email@gmail.com'
    password = raw_input()
    
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.ehlo()
    smtp.login(email, password)
    
    for user in sorted(users):
	if not users[user].has_key('servers'):
	   continue

	servers = users[user]['servers']
	destination = users[user]['email']

    	messenger = "\r\n".join(["From: %s" % email, "To: %s" % destination, "Subject: Just a message", "", "Why, oh why"])
   	smtp.sendmail(email, [destination], messenger)  
   
    smtp.close()

def main():
    kscreds = get_keystone_credentials()
    keystone = keystoneclient.Client(**kscreds)
    nvcreds = get_nova_credentials()
    nova = novaclient.Client(**nvcreds)

    users = get_users(keystone, nova)
    send_email(users)

if __name__ == '__main__':
   main()
