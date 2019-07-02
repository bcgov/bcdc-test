'''
Created on July 2, 2019

@author: crigdon

fixtures used to set up and tear down resource tests
'''


import logging
import pytest
import ckanapi


logger = logging.getLogger(__name__)

# --------------------- Supporting Functions ----------------------


def resource_exists(remote_api, test_resource_name, resource_get_id_fixture):
    '''
    :param remote_api: ckanapi, remote api object that is to be used to determine
                       if the package exists.
    :param test_resource_name:
    :param resource_get_id_fixture:
    '''

    res_exists = False
    try:
        res_data = remote_api.action.package_show(id=resource_get_id_fixture)
        logger.debug("resource show: %s", res_data)
        if res_data['name'] == test_resource_name:
            res_exists = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)

    return res_exists


# --------------------- Fixtures ----------------------


@pytest.fixture
def resource_get_id_fixture(remote_api_admin_auth, test_resource_name):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with auth
    :param test_resource_name: test resource name
    '''
    res_data = remote_api_admin_auth.action.resource_search(query="name:{0}".format(test_resource_name))
    logger.debug("resource_data: %s", res_data)
    res_id = res_data['results'][0]['id']
    logger.debug("resource_id: %s", res_id)

    yield res_id


@pytest.fixture
def resource_exists_fixture(remote_api_admin_auth, test_resource_name):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with authenticated
    :param test_resource_name: the name of a package that exists
    '''
    logger.debug("testing existence of package: %s", test_resource_name)
    exists = resource_exists(remote_api_admin_auth, test_resource_name)
    yield exists