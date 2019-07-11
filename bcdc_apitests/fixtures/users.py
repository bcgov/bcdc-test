'''
Created on July 08, 2019

@author: crigdon

Code used to boot users.
'''

import logging
import ckanapi
import pytest
from fixtures.ckan import remote_api_super_admin_auth

LOGGER = logging.getLogger(__name__)

# --------------------- Supporting Functions ----------------------

# TODO: might be able to set this up in the automatic parameterization, and 
#       move to a fixture so that it can be re-used.
#pylint: disable=unsubscriptable-object

def get_user_data(remote_api, user):
    '''
    use the super admin to get the user info as other api tokens may not 
    '''
    usr_data = {}
    try:
        LOGGER.debug("looking for the user: %s", user)
        usr_data = remote_api.action.user_show(id=user)
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)
    return usr_data

def check_if_user_exist(remote_api_admin_auth, user):
    usr_data = {}
    usr_exists = False
    usr_data = get_user_data(remote_api_admin_auth, user)
    LOGGER.debug("usr_data: %s", usr_data)
    if ('name' in usr_data) and usr_data['name'] == user:  
        usr_exists = True
    return usr_exists


def check_if_user_active(remote_api_admin_auth, user):
    usr_active = False
    usr_data = get_user_data(remote_api_admin_auth, user)
    if usr_data['state'] == "deleted":
        usr_active = True
    return usr_active


def user_delete(remote_api_admin_auth, user):
    try:
        usr_data = remote_api_admin_auth.action.user_delete(id=user)
        LOGGER.debug("delete user: %s", user)
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)


def assign_user_role(remote_api_admin_auth, user, org_id, role):
    resp = remote_api_admin_auth.action.organization_member_create(
        id=org_id, username=user, role=role)
    LOGGER.debug("setting test user role: %s", resp)


@pytest.fixture(scope="session")
def user_setup_fixture(org_setup_fixture, remote_api_super_admin_auth,
                       test_roles, temp_user_password):
    users = test_roles.keys()
    for user in users:
        email = test_roles[user]['email']
        exists = check_if_user_exist(remote_api_super_admin_auth, user)
        role = test_roles[user]['role']
        LOGGER.debug("user name: %s", user)
        LOGGER.debug("user role: %s", role)
        if exists:
            active = check_if_user_active(remote_api_super_admin_auth, user)
            if not active:
                LOGGER.debug("user %s not active", user)
                usr_data = remote_api_super_admin_auth.action.user_update(
                    id=user, state='active', email=email)
                LOGGER.debug("user found and changed state to: %s",
                             usr_data['state'])
        else:
            LOGGER.debug("attempting to create new user: %s", user)
            usr_data = remote_api_super_admin_auth.action.user_create(
                name=user, email=email,
                password=temp_user_password)
            LOGGER.debug("created user: %s", str(usr_data))
        org_id = org_setup_fixture['id']
        LOGGER.debug('org_id: %s', org_id)
        assign_user_role(remote_api_super_admin_auth, user, org_id, role)
    yield
    for user in users:
        user_delete(remote_api_super_admin_auth, user)

    
@pytest.fixture()
def user_data_fixture(remote_api_super_admin_auth, user_label_fixture):
    '''
    use the super admin to get the user info as other api tokens may not 
    '''
    usr_data = get_user_data(remote_api_super_admin_auth, user_label_fixture)
    return usr_data


