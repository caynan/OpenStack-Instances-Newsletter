#!/usr/bin/env python
import os

def get_keystone_creds():
    kwargs = {}
#   kwargs['user_domain_name'] = os.environ['OS_USER_DOMAIN_NAME']
    kwargs['username'] = os.environ['OS_USERNAME']
    kwargs['password'] = os.environ['OS_PASSWORD']
#   kwargs['project_domain_name'] = os.environ['OS_PROJECT_DOMAIN_NAME']
    kwargs['auth_url'] = os.environ['OS_AUTH_URL']
    kwargs['tenant_name'] = os.environ['OS_TENANT_NAME']
    return kwargs

def get_nova_creds():
    kwargs = {}
    kwargs['username'] = os.environ['OS_USERNAME']
    kwargs['api_key'] = os.environ['OS_PASSWORD']
    kwargs['auth_url'] = os.environ['OS_AUTH_URL']
    kwargs['project_id'] = os.environ['OS_TENANT_NAME']
    return kwargs
