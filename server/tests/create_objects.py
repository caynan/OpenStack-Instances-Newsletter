import keystoneclient.v2_0.client as ksclient
import novaclient.client as nvclient
import re
import sys
sys.path.append('../script')
from credentials import *

kscreds = get_keystone_credentials()
keystone = ksclient.Client(**kscreds)


def create_project(project_name, project_description = ""):
    """ Create a project.

    Keyword arguments:
    project_name -- name of the new project
    project_description -- description of the new project (default 'blank') 
    """
    if project_name == None or len(project_name) == 0:
        print "Error, project name cannot be blank."
	
    try:
	keystone.tenants.create(tenant_name = project_name, 
				description = project_description)
    except:
	print "Project '%s' cannot be created, check if already exist another project with this name." % project_name


def delete_project(project_name):
    """ Delete an existing project.

    Keyword arguments:
    project_name -- name of the project to be deleted
    """
    try:
        project = keystone.tenants.find(name = project_name)
        project_id = project.id
    except:
        print "Project '%s' does not exist." % project_name
        return

    keystone.tenants.delete(project_id)


def create_user(user_name, user_password, user_email, user_project = "demo"):
    """ Create an user.

    Keyword arguments:
    user_name -- name of the new user
    user_password -- password of the new user
    user_email -- email of the new user
    user_project -- project where user will be included (default "demo")
    """	
    if user_name == None or len(user_name) == 0:
        print "Error, user name cannot be blank."
        return

    if user_password == None or len(user_password) == 0:
	print "Error, password cannot be blank."
	return

    if user_email == None or not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user_email):
	print "Error, invalid email."
	return

    try:
	project = keystone.tenants.find(name = user_project)
	project_id = project.id
    except:
	print "Project '%s' does not exist." % user_project
	return
	
    try:
	keystone.users.create(name = user_name, password = user_password, 
			      email = user_email, tenant_id = project_id)
    except:
	print "User '%s' cannot be created, check if already exist another user with this name." % user_name


def delete_user(user_name):
    """ Delete an existing user.

    Keyword arguments:
    user_name -- name of the user to be deleted
    """
    try:
	user = keystone.users.find(name = user_name)
	user_id = user.id
    except:
	print "User '%s' does not exist." % user_name
	return
	
    keystone.users.delete(user_id)


def add_admin_role(user_name, project_name = "demo"):
    """ Assign admin role to an user.

    Keyword arguments:
    user_name -- user to receive admin role
    project_name -- user's project (default "demo") 
    """
    try:
        user = keystone.users.find(name = user_name)
    except:
        print "User '%s' does not exist." % user_name
        return

    try:
        project = keystone.tenants.find(name = project_name)
        project_id = project.id
    except:
        print "Project '%s' does not exist." % project_name
        return
	
    admin_role = keystone.roles.find(name = "admin")
    try:
	keystone.roles.add_user_role(user, admin_role, project_id)
    except:
	print "User '%s' already have admin role." % user_name


def remove_admin_role(user_name, project_name = "demo"):
    """ Remove admin role from an user.

    Keyword arguments:
    user_name -- user from where admin role will be removed
    project_name -- user's project (default "demo")
    """
    try:
        user = keystone.users.find(name = user_name)
    except:
        print "User '%s' does not exist." % user_name
        return

    try:
        project = keystone.tenants.find(name = project_name)
        project_id = project.id
    except:
        print "Project '%s' does not exist." % project_name
        return

    admin_role = keystone.roles.find(name="admin")
    try:
	keystone.roles.remove_user_role(user, admin_role, project_id)
    except:
	print "User '%s' does not have admin role." % user_name		

	
def create_instance(user_name, user_password, user_project, instance_name, flavor_name):
    """ Create an instance.
	
    Keyword arguments:
    user_name -- name of the user who will own the new instance.
    user_password -- password of the user who will own the new instance.
    user_project -- project of the user who will own the new instance.
    instance_name -- name of the new instance.
    flavor_name -- flavor of the new instance.  
    """
    try:
        user = keystone.users.find(name = user_name)
    except:
        print "User '%s' does not exist." % user_name
        return

    try:
        project = keystone.tenants.find(name = user_project)
    except:
        print "Project '%s' does not exist." % user_project
        return

    try:
	temp_nova = nvclient.Client("2", auth_url = kscreds['auth_url'], username = user_name,
                       	            api_key = user_password, project_id = user_project)
    except:
	print "Invalid user/password."
	return	
	
    image = temp_nova.images.list()[0]
	
    try:
	flavor = temp_nova.flavors.find(name = flavor_name)
    except:
	print "Flavor '%s' does not exist." % flavor_name
	return		

    temp_nova.servers.create(name = instance_name, image = image, flavor = flavor)


def delete_instance(user_name, user_password, user_project, instance_id):
    """ Delete an existing instance.
        
    Keyword arguments:
    user_name -- name of the owner of the instance to be deleted.
    user_password -- password of the owner of the instance to be deleted.
    user_project -- project of the owner of the instance to be deleted.
    instance_id -- id of the instance to be deleted.
    """
    try:
        user = keystone.users.find(name = user_name)
    except:
        print "User '%s' does not exist." % user_name
        return

    try:
        project = keystone.tenants.find(name = user_project)
    except:
        print "Project '%s' does not exist." % user_project
        return

    try:
	temp_nova = nvclient.Client("2", auth_url = kscreds['auth_url'], username = user_name,
                                    api_key = user_password, project_id = user_project)
    except:
	print "Invalid user/password."
	return
	
    try:
	temp_nova.servers.delete(instance_id)
    except:
	print "Instance id '%s' does not exist." % instance_id
