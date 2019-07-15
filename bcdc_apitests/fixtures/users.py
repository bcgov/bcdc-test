'''
Created on July 08, 2019

@author: crigdon

Code used to boot users.
'''

import logging
import ckanapi
import pytest
import time
from bcdc_apitests.fixtures.ckan import remote_api_super_admin_auth

LOGGER = logging.getLogger(__name__)

# --------------------- Supporting Functions ----------------------

# TODO: might be able to set this up in the automatic parameterization, and
#       move to a fixture so that it can be re-used.
# pylint: disable=unsubscriptable-object


def get_user_data(remote_api, user, retry=0):
    '''
    use the super admin to get the user info as other api tokens may not
    '''
    usr_data = {}
    try:
        LOGGER.debug("looking for the user: %s", user)
        usr_data = remote_api.action.user_show(id=user)
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)
    except ckanapi.errors.CKANAPIError:
        # seems like CKAN randomly fails with 500 every so often if you hit it
        # too hard.  This is an attempt to overcome that.
        retry += 1
        time.sleep(2)
        if retry == 3:
            raise
        get_user_data(remote_api, user, retry)
    return usr_data


def check_if_user_exist(remote_api_admin_auth, user):
    '''
    '''
    usr_data = {}
    usr_exists = False
    usr_data = get_user_data(remote_api_admin_auth, user)
    LOGGER.debug("usr_data: %s", usr_data)
    if ('name' in usr_data) and usr_data['name'] == user:
        usr_exists = True
    return usr_exists


def check_if_user_active(remote_api_admin_auth, user):
    usr_active = True
    usr_data = get_user_data(remote_api_admin_auth, user)
    if usr_data['state'] == "deleted":
        usr_active = False
    return usr_active


def user_delete(remote_api_admin_auth, user):
    try:
        usr_data = remote_api_admin_auth.action.user_delete(id=user)
        LOGGER.debug("retruned data: %s", usr_data)
        LOGGER.debug("delete user: %s", user)
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)


def assign_user_role(remote_api_admin_auth, user, org_id, role):
def get_user_apikey(remote_api_admin_auth,user):
    # func must run as sysadmin to return apikey of user
    usr_apiKey = ()
        logger.debug("setting test user role: %s", usr_data)
        usr_data = remote_api_admin_auth.action.user_show(id=user)
    try:
        usr_apiKey = usr_data['apikey']
    except ckanapi.errors.NotFound as err:
    return usr_apiKey
        logger.debug("err: %s %s", type(err), err)

    
    resp = remote_api_admin_auth.action.organization_member_create(
        id=org_id, username=user, role=role)
    LOGGER.debug("setting test user role: %s", resp)


@pytest.fixture(scope="session")
def user_setup_fixture(org_setup_fixture, remote_api_super_admin_auth,
                       test_roles, temp_user_password):
    
    # TODO: This is currently set up to create all the possible user types, 
    #       could set up as a function scope that creates and configures 
    #       users as required.  Caches results so that it doesn't have 
    #       to re-create.
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
        LOGGER.debug('user %s setup complete', user)
    yield
    #TODO: commenting out for now
#     for user in users:
#         user_delete(remote_api_super_admin_auth, user)


@pytest.fixture()
def user_data_fixture(remote_api_super_admin_auth, user_label_fixture):
    '''
    use the super admin to get the user info as other api tokens may not
    '''
    LOGGER.debug("user_label_fixture: %s", user_label_fixture)
    usr_data = get_user_data(remote_api_super_admin_auth, user_label_fixture)
    return usr_data


@pytest.fixture(scope='session')
def user_data_fixture_session(remote_api_super_admin_auth, user_label_fixture):
    '''
    use the super admin to get the user info as other api tokens may not
    '''
    LOGGER.debug("user_label_fixture: %s / %s", user_label_fixture,
                 type(user_label_fixture))
    if isinstance(user_label_fixture, list):
        if len(user_label_fixture) <> 1:
            msg = 'Received more than one user in the user_label_fixture.  ' + \
                  'fixture is only configured to deal with 1 user at a time.' + \
                  'user labels: %s'
            msg = msg.format(user_label_fixture)
            raise TooManyUsersException(msg)
        user_label_fixture = user_label_fixture[0]
    usr_data = get_user_data(remote_api_super_admin_auth, user_label_fixture)
    return usr_data

class TooManyUsersException(Exception):
    pass


    