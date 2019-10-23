'''
Created on July 08, 2019

@author: crigdon

Code used to boot users.
'''

import logging
import time

import ckanapi
import pytest

# from bcdc_apitests.fixtures.ckan import remote_api_super_admin_auth
# from bcdc_apitests.fixtures.config_fixture import test_roles

# adding imports here to allow ide code navigation even though they are already
# declared in the conftest.py
LOGGER = logging.getLogger(__name__)

# --------------------- Supporting Functions ----------------------

# pylint: disable=redefined-outer-name


def get_user_data(remote_api, user, retry=0):
    '''
    :param remote_api: a ckanapi RemoteAPI object with super admin authentication
    :param user: the name fo the user that we are looking for
    :param retry:  the number of times to retry before fail, implemented this
        because the api was being flaky and failing on the first attempt

    using the remote_api gets the data associated with a specific user
    '''
    usr_data = {}
    try:
        LOGGER.debug("looking for the user: %s", user)
        usr_data = remote_api.action.user_show(id=user)
        LOGGER.debug("usr_data: %s", usr_data)
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
    :param remote_api: a ckanapi RemoteAPI object with super admin authentication
    :param user: the name fo the user that we are looking for
    :return: a boolean indicating if the "user" exists.
    '''
    usr_exists = False
    usr_data = get_user_data(remote_api_admin_auth, user)
    LOGGER.debug("usr_data: %s", usr_data)
    if ('name' in usr_data) and usr_data['name'] == user:
        usr_exists = True
    return usr_exists


def check_if_user_active(remote_api_admin_auth, user):
    '''
    :param remote_api_admin_auth: a ckanapi.RemoteAPI object with authorization
    :param user: the name of the user that we are searching for.
    :return: boolean indicating if the user exists and is active
    '''
    usr_active = True
    usr_data = get_user_data(remote_api_admin_auth, user)
    if usr_data['state'] == "deleted":
        usr_active = False
    return usr_active


def user_delete(remote_api_admin_auth, user):
    '''
    :param remote_api_admin_auth: a ckanapi.RemoteAPI object with authorization
    :param user: the name of the user that we are going to delete.
    '''
    try:
        usr_data = remote_api_admin_auth.action.user_delete(id=user)
        LOGGER.debug("retruned data: %s", usr_data)
        LOGGER.debug("delete user: %s", user)
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)
        

def assign_user_role(remote_api_admin_auth, user, org_id, role):
    '''
    :param remote_api_admin_auth: a ckanapi.RemoteAPI object with authorization
    :param user: the name of the user that we are going to delete.
    :param org_id: the organization id that a user should be a part of
    :param role: the role that the user should be assigned to.
    '''
    resp = remote_api_admin_auth.action.organization_member_create(
        id=org_id, username=user, role=role)
    LOGGER.debug("setting test user role: %s", resp)


@pytest.fixture(scope="session")
def user_setup_fixture(group_setup_fixture, remote_api_super_admin_auth,
                       test_roles, temp_user_password,
                       cancel_user_teardown):
    '''
    Used in session setup and tear down.  Creates the 3 test users that are
    used by tests.
    
    This fixture is required for the org fixture org_setup_fixture.. This code
    runs first then the orgs are configured, where the users are made part 
    of the test org
    '''
    # removed fixture dep org_setup_fixture
    users = test_roles.keys()
    user_names = []
    users_for_org = []
    for user in users:
        email = test_roles[user]['email']
        exists = check_if_user_exist(remote_api_super_admin_auth, user)
        role = test_roles[user]['role']
        users_for_org.append({"capacity": role, "name": user})

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
    yield users_for_org
    if not cancel_user_teardown:
        for user in users:
            LOGGER.debug(f"user {user} deleted")
            user_delete(remote_api_super_admin_auth, user)
            
@pytest.fixture()
def user_data_fixture(remote_api_super_admin_auth, user_label_fixture):
    '''
    use the super admin to get the user info as other api tokens may not
    '''
    LOGGER.debug("user_label_fixture: %s", user_label_fixture)
    usr_data = get_user_data(remote_api_super_admin_auth, user_label_fixture[0])
    yield usr_data


@pytest.fixture(scope='session')
def user_data_fixture_session(remote_api_super_admin_auth, user_label_fixture):
    '''
    use the super admin to get the user info as other api tokens may not
    '''
    LOGGER.debug("user_label_fixture: %s / %s", user_label_fixture,
                 type(user_label_fixture))
    if isinstance(user_label_fixture, list):
        if len(user_label_fixture) != 1:
            msg = 'Received more than one user in the user_label_fixture.  ' + \
                  'fixture is only configured to deal with 1 user at a time.' + \
                  'user labels: %s'
            msg = msg.format(user_label_fixture)
            raise TooManyUsersException(msg)
        user_label_fixture = user_label_fixture[0]
    usr_data = get_user_data(remote_api_super_admin_auth, user_label_fixture)
    yield usr_data


class TooManyUsersException(Exception):
    '''
    raised when multiple users are returned, when expecting a single user
    '''
    pass
