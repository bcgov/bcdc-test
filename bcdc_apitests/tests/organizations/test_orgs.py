'''
Created on May 16, 2019

@author: KJNETHER

Can't test orgs as there is no way to create orgs without superuser


'''
import logging
import ckanapi
import pytest

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name


def test_verify_read_orgs(ckan_url):
    '''
    verifies can retrieve a list of organizations and that there is at least
    one org defined
    '''
    remote_api = ckanapi.RemoteCKAN(ckan_url)
    pkg_list = remote_api.action.organization_list()
    LOGGER.debug("orglist cnt: %s", len(pkg_list))
    assert pkg_list


def test_org_create_if_not_exists(remote_api_admin_auth, test_organization, org_exists_fixture, test_org_data):
    '''
    requires sysadmin to create orgs
    test for org, if does not exist lets create one
    '''

    if org_exists_fixture:
        org_data = remote_api_admin_auth.action.organization_show(id=test_organization)
        LOGGER.debug("org_exists: %s", org_data)
    else:
        org_data = remote_api_admin_auth.action.organization_create(**test_org_data)
        LOGGER.debug("create org: %s", org_data)


def test_verify_test_org_exists(ckan_url, ckan_apitoken, test_organization):
    '''
    verifies that the test_organization exists, if not create
    '''
    org = ''
    remote_api = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
    try:
        org = remote_api.action.organization_show(id=test_organization)
    except ckanapi.errors.NotFound as err:
        msg = 'The test organization {0} that is required for most tests does ' + \
              'not exist'
        LOGGER.debug("error: %s", type(err))
        msg = msg.format(test_organization)
        LOGGER.error(msg)
        pytest.fail(msg)
    LOGGER.debug("org: %s", org)


#No need to purge org at this level
# def test_org_purge(org_teardown_fixture):
#     org = org_teardown_fixture
#     LOGGER.debug('post cleanup: %s', org)

