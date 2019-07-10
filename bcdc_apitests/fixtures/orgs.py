'''
Created on May 29, 2019

@author: crigdon

Code used to verify orgs.
'''

import logging
import ckanapi
import pytest

logger = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name

# --------------------- Supporting Functions ----------------------


def org_delete(remote_api, test_organization):

    logger.debug("deleting the org: %s", test_organization)
    remote_api.action.organization_delete(id=test_organization)


def org_purge(remote_api, test_organization):

    logger.debug("purging the org: %s", test_organization)
    remote_api.action.organization_purge(id=test_organization)


def org_exists(remote_api, test_organization):
    org_exists = False
    try:
        org_data = remote_api.action.organization_show(id=test_organization)
        logger.debug("org found and show: %s", org_data)
        if org_data['name'] == test_organization:
            org_exists = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)

    return org_exists


def org_create_if_not_exists(remote_api, test_organization, test_org_data):

    exists = org_exists(remote_api, test_organization)
    if exists:
        org_data = remote_api.action.organization_show(id=test_organization)
    else:
        org_data = remote_api.action.organization_create(**test_org_data)
        logger.debug("org_return: %s", org_data)
    return org_data


def org_purge_if_exists(remote_api, test_organization):

    exists = org_exists(remote_api, test_organization)
    if exists:
        org_purge(remote_api, test_organization)


# --------------------- Fixtures ----------------------

@pytest.fixture
def org_create_fixture(remote_api_admin_auth, test_org_data):
    org_return = remote_api_admin_auth.action.organization_create(**test_org_data)
    logger.debug("org_return: %s", org_return)
    yield org_return

@pytest.fixture
def org_create_if_not_exists_fixture(remote_api_admin_auth, test_organization, org_exists_fixture, test_org_data):
    logger.debug("test_org_exists: %s %s", org_exists_fixture, type(org_exists_fixture))

    if org_exists_fixture:
        org_data = remote_api_admin_auth.action.organization_show(id=test_organization)
    else:
        org_data = remote_api_admin_auth.action.organization_create(**test_org_data)
        logger.debug("org_return: %s", org_data)
    yield org_data


@pytest.fixture
def org_exists_fixture(remote_api_admin_auth, test_organization):

    logger.debug("testing existence of org: %s", test_organization)
    exists = org_exists(remote_api_admin_auth, test_organization)
    yield exists

@pytest.fixture
def org_id_fixture(remote_api_admin_auth, test_organization):

    logger.debug("get id of org: %s", test_organization)

    org_data = remote_api_admin_auth.action.organization_show(id=test_organization)

    # get org id
    org_id = org_data['id']
    logger.debug("ID is : %s", org_id)

    yield org_id

@pytest.fixture
def org_teardown_fixture(remote_api_admin_auth, test_organization):

    org_delete(remote_api_admin_auth, test_organization)
    logger.debug("initial delete of org : %s", test_organization)
    org_purge(remote_api_admin_auth, test_organization)
    logger.debug("initial purge of org : %s", test_organization)

