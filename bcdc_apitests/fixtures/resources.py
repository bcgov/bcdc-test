'''
Created on July 2, 2019

@author: crigdon

fixtures used to set up and tear down resource tests
'''

import logging
import pytest
import ckanapi
# from bcdc_apitests.fixtures.ckan import remote_api_super_admin_auth

LOGGER = logging.getLogger(__name__)

# pylint: disable=redefined-outer-name

# --------------------- Supporting Functions ----------------------


def resource_exists(remote_api, resource_name,
                    resource_id):
    '''
    :param remote_api: ckanapi, remote api object that is to be used to determine
                       if the package exists.
    :param test_resource_name:
    :param resource_get_id_fixture:
    '''

    res_exists = False
    try:
        res_data = remote_api.action.package_show(id=resource_id)
        LOGGER.debug("resource show: %s", res_data)
        if res_data['name'] == resource_name:
            res_exists = True
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)

    return res_exists


def get_resource(remote_api, resource_name, pkg_id):
    '''
    :param remote_api: a ckanapi remote object, w/ credentials
    :param resource_name: the name of the resource
    :param pkg_id: the package id or package name that the resource should be
        a part of.
    '''
    pkg_data = remote_api.action.package_show(id=pkg_id)
    res_data = None
    if 'resources' in pkg_data:
        for rsrc in pkg_data['resources']:
            if rsrc['name'] == resource_name:
                res_data = rsrc
                break
    return res_data


def resource_teardown(remote_api, pkg_name):
    '''
    a helper method with the code required to cleanup the resources that are
    created for the testing
    :param remote_api: a ckanapi.RemoteAPI object with auth headers
    :param pkg_name: the name of the test package that the resource is
        a part of
    '''
    pkg_data = remote_api.action.package_show(id=pkg_name)
    LOGGER.debug("pkg_data: %s", pkg_data)
    for rsrc in pkg_data['resources']:
        LOGGER.debug("deleting resource: %s", rsrc['name'])
        remote_api.action.resource_delete(id=rsrc['id'])
    LOGGER.debug("deleting package: %s", pkg_name)
    remote_api.action.package_delete(id=pkg_name)

# --------------------- Fixtures ----------------------


@pytest.fixture
def resource_get_id_fixture(get_resource_fixture):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with auth
    :param test_resource_name: test resource name
    '''
    res_id = get_resource_fixture['results'][0]['id']
    LOGGER.debug("resource_id: %s", res_id)
    yield res_id


@pytest.fixture
def get_resource_fixture(res_create_if_not_exists,
                         remote_api_super_admin_auth, test_resource_name):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with auth
    :param test_resource_name: test resource name
    '''
    res_data = remote_api_super_admin_auth.action.resource_search(
        query="name:{0}".format(test_resource_name))
    LOGGER.debug("resource_data: %s", res_data)
    yield res_data


@pytest.fixture
def res_create_if_not_exists(package_create_if_not_exists,
                             remote_api_super_admin_auth,
                             test_resource_name, resource_data):
    '''
    Checks to see if the resource exists and creates it if does not

    :param package_create_if_not_exists: creates the package if it doesn't exist
        resources are added to packages so the package needs to exist.
    :param remote_api_super_admin_auth:
    '''
    pkgid = package_create_if_not_exists['id']
    resource = get_resource(remote_api_super_admin_auth, test_resource_name,
                            pkgid)
    if not resource:
        resource = remote_api_super_admin_auth.action.resource_create(**resource_data)
        LOGGER.debug("created resource: %s", resource)
    yield resource


@pytest.fixture
def resource_delete_if_exists(package_create_if_not_exists,
                              remote_api_super_admin_auth):
    '''
    deletes all the resources from the test package
    '''
    # thinking just delete all the resources from the package
    if 'resources' in package_create_if_not_exists:
        for rsrc in package_create_if_not_exists['resources']:
            LOGGER.debug("rsrc: %s", rsrc)
            LOGGER.debug("rsrc id: %s", rsrc['id'])
            remote_api_super_admin_auth.action.resource_delete(id=rsrc['id'])
    yield


@pytest.fixture
def resource_exists_fixture(package_create_if_not_exists,
                            remote_api_super_admin_auth, test_resource_name):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with authenticated
    :param test_resource_name: the name of a package that exists
    '''
    pkgid = package_create_if_not_exists['id']
    exists = resource_exists(remote_api_super_admin_auth, test_resource_name,
                             pkgid)
    yield exists
