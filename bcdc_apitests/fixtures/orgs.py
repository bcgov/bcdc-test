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

    LOGGER.debug("deleting the org: %s", test_organization)
    remote_api.action.organization_delete(id=test_organization)

def org_purge(remote_api, test_organization):

    LOGGER.debug("purging the org: %s", test_organization)
    remote_api.action.organization_purge(id=test_organization)

def org_exists(remote_api, test_organization):
    org_exists = False
    try:
        org_data = remote_api.action.organization_show(id=test_organization)
        LOGGER.debug("org found and show: %s", org_data)
        if org_data['name'] == test_organization:
            org_exists = True
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)

    return org_exists

# --------------------- Fixtures ----------------------

@pytest.fixture
def org_create_fixture(remote_api_super_admin_auth, test_org_data):
    org_return = remote_api_super_admin_auth.action.organization_create(**test_org_data)
    LOGGER.debug("org_return: %s", org_return)
    yield org_return

@pytest.fixture
def org_create_if_not_exists_fixture(remote_api_super_admin_auth, test_organization, org_exists_fixture, test_org_data):
    LOGGER.debug("test_org_exists: %s %s", org_exists_fixture, type(org_exists_fixture))
    LOGGER.debug("test_organization: %s", test_organization)
    if org_exists_fixture:
        org_data = remote_api_super_admin_auth.action.organization_show(id=test_organization)
    else:
        org_data = remote_api_super_admin_auth.action.organization_create(**test_org_data)
        LOGGER.debug("org_return: %s", org_data)
    yield org_data

@pytest.fixture(scope='session')
def org_exists_fixture(remote_api_super_admin_auth, test_organization):

    LOGGER.debug("testing existence of org: %s", test_organization)
    exists = org_exists(remote_api_super_admin_auth, test_organization)
    yield exists
    
    
    
@pytest.fixture
def org_id_fixture(remote_api_super_admin_auth, test_organization):

    LOGGER.debug("get id of org: %s", test_organization)

    org_data = remote_api_super_admin_auth.action.organization_show(id=test_organization)

    # get org id
    org_id = org_data['id']
    LOGGER.debug("ID is : %s", org_id)
    yield org_id

@pytest.fixture
def org_teardown_fixture(remote_api_super_admin_auth, test_organization):

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
    '''
    LOGGER.debug("Setup Org: %s", test_session_organization)
    org_data = None
    if not org_exists_fixture:
        org_data = remote_api_super_admin_auth.action.organization_create(
            **session_test_org_data)
        LOGGER.debug("org_data: %s", org_data)
    yield org_data
    LOGGER.debug("Cleanup Org: %s", test_session_organization)
    org_purge(remote_api_super_admin_auth, test_session_organization)
    LOGGER.debug("Org is purged: %s", test_session_organization)
    

