'''
Created on Sept 05, 2019

@author: crigdon

Code used to verify groups.
'''

import logging
import ckanapi
import pytest

LOGGER = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name, logging-fstring-interpolation


# TODO: possibly move supporting functions to helper package
# --------------------- Supporting Functions ----------------------


# need to be able to call directly... don't need to make this a fixture.
def group_delete(remote_api, test_group):
    '''
    makes call to group_delete to remove the group that gets set up for
    testing
    :param test_group: the name of the test group that is to be
        deleted.
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    '''
    LOGGER.debug("deleting the group: %s", test_group)
    remote_api.action.group_delete(id=test_group)


def group_purge(remote_api, test_group):
    '''
    :param test_group: the name of the test group that is to be
        purged
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    '''

    LOGGER.debug("purging the group: %s", test_group)
    remote_api.action.group_purge(id=test_group)


def group_exists(remote_api, test_group):
    '''
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    :param test_group: the name of the test group who's existence
        is to be determined
    '''
    group_exists = False
    try:
        group_data = remote_api.action.group_show(id=test_group)
        LOGGER.debug("group found and show: %s", group_data)
        if group_data['name'] == test_group:
            group_exists = True
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)

    return group_exists


def group_create_if_not_exists(remote_api, test_group, test_group_data):
    '''
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    :param test_group: the name of the test organization who's existence
        is to be determined
    :param test_org_data: a dictionary containing the data to be used to create
        a test group
    '''
    exists = group_exists(remote_api, test_group)
    if exists:
        group_data = remote_api.action.group_show(id=test_group)
    else:
        group_data = remote_api.action.group_create(**test_group_data)
        LOGGER.debug("group_return: %s", group_data)
    return group_data


def group_purge_if_exists(remote_api, test_group):
    '''
    if the group: test_group exists it will be purged
    :param test_group: the name of the group that is to be purged
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    '''

    exists = group_exists(remote_api, test_group)
    if exists:
        group_purge(remote_api, test_group)


def group_un_delete(remote_api, test_group):
    '''
    :param remote_api: ckanapi remote with authentication
    :param test_group: name of the test group to set state back to 'active'
    '''
    update_val = {'state': 'active',
                  'id': test_group}
    ret_val = remote_api.action.group_patch(**update_val)
    LOGGER.debug("ret_val: %s", ret_val)

# --------------------- Fixtures ----------------------


@pytest.fixture
def group_create_fixture(remote_api_super_admin_auth, test_group_data):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_group_data: the data that is to be used to create the test
        group

    '''
    group_return = remote_api_super_admin_auth.action.group_create(
        **test_group_data)
    LOGGER.debug("group_return: %s", group_return)
    yield group_return


@pytest.fixture
def group_create_if_not_exists_fixture(remote_api_super_admin_auth,
                                       test_group, group_exists_fixture,
                                       test_group_data):
    '''
    group may not show as existing even though it actually exists, its just in
    a state where it doesn't show up in either group_show or group_list.  To
    deal with this condition, catch ValidationError, purge, then try to
    recreate

    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_group: the name of the group that is to be purged
    :param group_exists_fixture: boolean indicating if the test group
        exists
    :param test_group_data: the data that is to be used to create the test
        group
    '''
    LOGGER.debug("test_group_exists: %s %s", group_exists_fixture,
                 type(group_exists_fixture))
    LOGGER.debug("test_group: %s", test_group)
    LOGGER.debug("test_group_data: %s", test_group_data)
    LOGGER.debug("group_exists_fixture: %s", group_exists_fixture)
    if group_exists_fixture:
        group_data = remote_api_super_admin_auth.action.group_show(
            id=test_group)
        LOGGER.debug("group_data retrieved: %s", group_data)
    else:
        try:
            LOGGER.debug('attempting to create the group: %s', test_group)
            group_data = remote_api_super_admin_auth.action.group_create(
                **test_group_data)
            LOGGER.debug("group_return: %s", group_data)
        except ckanapi.errors.ValidationError:
            LOGGER.debug('Trying a purge / then recreate for: %s',
                         test_group)
            group_purge(remote_api_super_admin_auth, test_group)
            group_data = remote_api_super_admin_auth.action.group_create(
                **test_group_data)
            LOGGER.debug("group_return: %s", group_data)
    # make sure that the group is not in a deleted state.
    group_un_delete(remote_api_super_admin_auth, test_group)
    yield group_data


@pytest.fixture(scope='session')
def group_exists_fixture(remote_api_super_admin_auth, test_group):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_group: the name of the group that is to be purged
    :return: boolean indicating if the group exists.
    '''
    LOGGER.debug("testing existence of group: %s", test_group)
    exists = group_exists(remote_api_super_admin_auth, test_group)
    yield exists


@pytest.fixture
def group_id_fixture(remote_api_super_admin_auth, test_group):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_group: the name of the group that is to be purged
    :return: the id that corresponds with the group name in the
        arg test_group
    '''
    LOGGER.debug("get id of group: %s", test_group)

    group_data = remote_api_super_admin_auth.action.group(id=test_group)

    # get group id
    group_id = group_data['id']
    LOGGER.debug("ID is : %s", group_id)
    yield group_id


@pytest.fixture
def group_teardown_fixture(remote_api_super_admin_auth, test_group, cancel_group_teardown):
    '''
    removes the test group at the conclusion of a test run.
    :param remote_api_super_admin_auth: remote ckanapi object with auth header
    :param test_group: name of the test group that is to be deleted
        and purged
    '''
    yield
    if not cancel_group_teardown:
        group_delete(remote_api_super_admin_auth, test_group)
        LOGGER.debug("initial delete of group : %s", test_group)
        group_purge(remote_api_super_admin_auth, test_group)
        LOGGER.debug("initial purge of group : %s", test_group)


@pytest.fixture(scope='session')
def group_setup_fixture(remote_api_super_admin_auth, test_session_group,
                        group_exists_fixture, session_test_group_data,
                        cancel_group_teardown):
    '''
    at start of tests will test to see if the required test group
    exists.  if it does not it gets created.  At conclusion of testing
    will clean it up with a delete.

    :param remote_api_super_admin_auth: remote ckanapi object with auth header
    :param test_session_group: the name of the group to be used for the
        test
    :param group_exists_fixture: does the group used for testing exist
    :param session_test_group_data: data to use when creating the group
    '''
    # was getting errors if this was not explicity set.
    session_test_group_data['is_organization'] = False
    session_test_group_data['type'] = "group"

    LOGGER.debug("Setup group: %s", test_session_group)
    LOGGER.debug(f"group session data: {session_test_group_data}")
    group_data = None
    if not group_exists_fixture:
        group_data = remote_api_super_admin_auth.action.group_create(
            **session_test_group_data)
        LOGGER.debug("group_data from create: %s", group_data)
    else:
        group_data = remote_api_super_admin_auth.action.group_show(
            id=session_test_group_data['name'])
        LOGGER.debug("group_data from show: %s", group_data)
    yield group_data

    if not cancel_group_teardown:
        LOGGER.debug("Cleanup group: %s", test_session_group)
        group_delete(remote_api_super_admin_auth, test_session_group)
        LOGGER.debug("group is purged: %s", test_session_group)
