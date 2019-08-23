'''
Created on May 29, 2019

@author: crigdon

Code used to verify orgs.
'''

import logging
import ckanapi
import pytest

LOGGER = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name

# TODO: possibly move supporting functions to helper package
# --------------------- Supporting Functions ----------------------


# need to be able to call directly... don't need to make this a fixture.
def org_delete(remote_api, test_organization):
    '''
    makes call to organization_delete to remove the org that gets set up for
    testing
    :param test_organization: the name of the test organization that is to be
        deleted.
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    '''
    LOGGER.debug("deleting the org: %s", test_organization)
    remote_api.action.organization_delete(id=test_organization)


def org_purge(remote_api, test_organization):
    '''
    :param test_organization: the name of the test organization that is to be
        purged
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    '''

    LOGGER.debug("purging the org: %s", test_organization)
    remote_api.action.organization_purge(id=test_organization)


def org_exists(remote_api, test_organization):
    '''
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    :param test_organization: the name of the test organization who's existence
        is to be determined
    '''
    org_exists = False
    try:
        org_data = remote_api.action.organization_show(id=test_organization)
        LOGGER.debug("org found and show: %s", org_data)
        if org_data['name'] == test_organization:
            org_exists = True
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)

    return org_exists


def org_create_if_not_exists(remote_api, test_organization, test_org_data):
    '''
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    :param test_organization: the name of the test organization who's existence
        is to be determined
    :param test_org_data: a dictionary containing the data to be used to create
        a test organization
    '''
    exists = org_exists(remote_api, test_organization)
    if exists:
        org_data = remote_api.action.organization_show(id=test_organization)
    else:
        org_data = remote_api.action.organization_create(**test_org_data)
        LOGGER.debug("org_return: %s", org_data)
    return org_data


def org_purge_if_exists(remote_api, test_organization):
    '''
    if the organization: test_organization exists it will be purged
    :param test_organization: the name of the organization that is to be purged
    :param remote_api: a remote ckan object with authorization key.
    :type remote_api: ckanapi.RemoteCKAN
    '''

    exists = org_exists(remote_api, test_organization)
    if exists:
        org_purge(remote_api, test_organization)

def org_un_delete(remote_api, test_organization):
    update_val = {'state': 'active', 
                  'id': test_organization}
    ret_val = remote_api.action.organization_patch(**update_val)
    LOGGER.debug("ret_val: %s", ret_val)

# --------------------- Fixtures ----------------------


@pytest.fixture
def org_create_fixture(remote_api_super_admin_auth, test_org_data):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_org_data: the data that is to be used to create the test
        organization

    '''
    org_return = remote_api_super_admin_auth.action.organization_create(
        **test_org_data)
    LOGGER.debug("org_return: %s", org_return)
    yield org_return


@pytest.fixture
def org_create_if_not_exists_fixture(remote_api_super_admin_auth,
                                     test_organization, org_exists_fixture,
                                     test_org_data):
    '''
    org may not show as existing even though it actually exists, its just in
    a state where it doesn't show up in either org_show or org_list.  To
    deal with this condition, catch ValidationError, purge, then try to
    recreate

    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_organization: the name of the organization that is to be purged
    :param org_exists_fixture: boolean indicating if the test organization
        exists
    :param test_org_data: the data that is to be used to create the test
        organization
    '''
    LOGGER.debug("test_org_exists: %s %s", org_exists_fixture,
                 type(org_exists_fixture))
    LOGGER.debug("test_organization: %s", test_organization)
    LOGGER.debug("test_org_data: %s", test_org_data)
    LOGGER.debug("org_exists_fixture: %s", org_exists_fixture)
    if org_exists_fixture:
        org_data = remote_api_super_admin_auth.action.organization_show(
            id=test_organization)
        LOGGER.debug("org_data retrieved: %s", org_data)
    else:
        try:
            LOGGER.debug('attempting to create the org: %s', test_organization)
            org_data = remote_api_super_admin_auth.action.organization_create(
                **test_org_data)
            LOGGER.debug("org_return: %s", org_data)
        except ckanapi.errors.ValidationError:
            LOGGER.debug('Trying a purge / then recreate for: %s',
                         test_organization)
            org_purge(remote_api_super_admin_auth, test_organization)
            org_data = remote_api_super_admin_auth.action.organization_create(
                **test_org_data)
            LOGGER.debug("org_return: %s", org_data)
    # make sure that the org is not in a deleted state.
    org_un_delete(remote_api_super_admin_auth, test_organization)
    yield org_data


@pytest.fixture(scope='session')
def org_exists_fixture(remote_api_super_admin_auth, test_organization):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_organization: the name of the organization that is to be purged
    :return: boolean indicating if the organization exists.
    '''
    LOGGER.debug("testing existence of org: %s", test_organization)
    exists = org_exists(remote_api_super_admin_auth, test_organization)
    yield exists


@pytest.fixture
def org_id_fixture(remote_api_super_admin_auth, test_organization):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_organization: the name of the organization that is to be purged
    :return: the id that corresponds with the organization name in the
        arg test_organization
    '''
    LOGGER.debug("get id of org: %s", test_organization)

    org_data = remote_api_super_admin_auth.action.organization_show(id=test_organization)

    # get org id
    org_id = org_data['id']
    LOGGER.debug("ID is : %s", org_id)
    yield org_id


@pytest.fixture
def org_teardown_fixture(remote_api_super_admin_auth, test_organization):
    '''
    removes the test organization at the conclusion of a test run.
    :param remote_api_super_admin_auth: remote ckanapi object with auth header
    :param test_organization: name of the test organization that is to be deleted
        and purged
    '''
    yield
    org_delete(remote_api_super_admin_auth, test_organization)
    LOGGER.debug("initial delete of org : %s", test_organization)
    org_purge(remote_api_super_admin_auth, test_organization)
    LOGGER.debug("initial purge of org : %s", test_organization)


@pytest.fixture(scope="session")
def org_setup_fixture(remote_api_super_admin_auth, test_session_organization,
                      org_exists_fixture, session_test_org_data):
    '''
    at start of tests will test to see if the required test org
    exists.  if it does not it gets created.  At conclusion of testing
    will clean it up with a delete.

    :param remote_api_super_admin_auth: remote ckanapi object with auth header
    :param test_session_organization: the name of the org to be used for the
        test
    :param org_exists_fixture: does the org used for testing exist
    :param session_test_org_data: data to use when creating the org
    '''
    LOGGER.debug("Setup Org: %s", test_session_organization)
    org_data = None
    if not org_exists_fixture:
        org_data = remote_api_super_admin_auth.action.organization_create(
            **session_test_org_data)
        LOGGER.debug("org_data from create: %s", org_data)
    else:
        org_data = remote_api_super_admin_auth.action.organization_show(
            id=session_test_org_data['name'])
        LOGGER.debug("org_data from show: %s", org_data)
    yield org_data
    
    LOGGER.debug("Cleanup Org: %s", test_session_organization)
    org_delete(remote_api_super_admin_auth, test_session_organization)
    LOGGER.debug("Org is purged: %s", test_session_organization)
