'''
Created on Jun. 11, 2019

@author: crigdon
'''

import logging
import requests
import ckanapi

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name


def test_resource_create(conf_fixture, ckan_url, ckan_rest_dir, ckan_auth_header,
                         resource_data, resource_delete_if_exists):
    '''
    add new resource

    :param ckan_url: domain to be used for ckan calls
    :param ckan_rest_dir: root path to the rest api
    :param ckan_auth_header: authorization header
    :param resource_data: the resource data to be used in the creation of a
        new resource object, creates the package if it doesn't exist, retrieves
        the package id, and adds it to the resource data
    :param resource_delete_if_exists: makes sure the package exists and does not
        have any resources associated with it.
    :param conf_fixture: the fixture parameterization configuration
    '''
    # define api call
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_create')
    LOGGER.debug('api_call: %s', api_call)

    # create resource
    res_data = requests.post(api_call, headers=ckan_auth_header, json=resource_data)
    LOGGER.debug("resource_create: %s", res_data.text)

    # get resource id
    resp_json = res_data.json()
    LOGGER.debug('resp_json: %s', resp_json)
    LOGGER.debug('res_data.status_code: %s', res_data.status_code)
    testStatus = res_data.status_code == 200
    LOGGER.debug("test status: %s", testStatus)
    assert testStatus == conf_fixture.test_result
    if testStatus:
        # if the we can successfully create the resource then make sure that
        # it shows up in a package_show
        # check is resource exist and shows up in resource_show
        # define remote api
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_show')
        res_id = resp_json['result']['id']
        res_data = requests.get(api_call, headers=ckan_auth_header,
                                params={'id':res_id})
        resp_json = res_data.json()
        assert resp_json['success'] == conf_fixture.test_result


# update resource
def test_resource_update(conf_fixture, ckan_url, ckan_rest_dir, ckan_auth_header,
                         resource_data, package_get_id_fixture,
                         resource_get_id_fixture):
    '''
    :param resource_data: test resource structure, this fixture will also make 
        sure that a test package exists that it can use for the testing.
    :param ckan_url: the ckan url to be used for the test
    :param ckan_rest_dir: the ckan rest dir to use for the test
    :param ckan_auth_header: auth header with api token configured for the 
        parameterized user
    :param package_get_id:
    :param resource_get_id_fixture:
    '''
    # update resource data dic with resource id
    resource_data['id'] = resource_get_id_fixture
    LOGGER.debug("resource_id: %s", resource_data['id'])

    # change some data in resource data dic
    resource_data['description'] = 'test resource_update'

    # define api
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_update')
    LOGGER.debug('api_call: %s', api_call)

    # update resource
    res_data = requests.post(api_call, headers=ckan_auth_header, json=resource_data)
    LOGGER.debug("resource_update: %s", res_data.text)

    assert (res_data.status_code == 200) == conf_fixture.test_result
    # the assuming returned 200 should make sure we can retrieve the changed 
    # data
    


# search resource
def test_resource_search(conf_fixture, remote_api_auth, test_resource_name):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    :param test_resource_name: test resource name
    '''
    # TODO: add a fixture that makes sure the resource has been created in case
    #      the tests above have failed to create one.
    # define remote api
    remote_api = remote_api_auth

    # search for resource by name
    res_data = remote_api.action.resource_search(query="name:{0}".format(
        test_resource_name))
    LOGGER.debug("resource search results: %s", res_data)

    assert (res_data['count'] >= 1) == conf_fixture.test_result


# delete resource
def test_resource_delete(conf_fixture, remote_api_auth, ckan_url,
                         ckan_rest_dir, ckan_auth_header, res_create_if_not_exists,
                         resource_get_id_fixture):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    :param resource_data: test resource structure
    :param ckan_url:
    :param ckan_rest_dir:
    :param ckan_auth_header:
    :param resource_get_id_fixture:
    '''
    # TODO: create add resource if not exists fixture, that should call 
    #       create package if not exists fixture, for valid package
    # define api
    remote_api = remote_api_auth
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_delete')
    resp = requests.post(api_call, headers=ckan_auth_header, 
                            json={'id': resource_get_id_fixture})
    resp_data = resp.json()
    LOGGER.debug("resp_data: %s", resp_data)
    assert (resp.status_code == 200) == conf_fixture.test_result
    
    if resp.status_code == 200:
        # check is resource exist
        # define api
        
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_show')
        LOGGER.debug('api_call: %s', api_call)
    
        # show resource
        res_data = requests.get(api_call, headers=ckan_auth_header, 
                                params={'id': resource_get_id_fixture})
        LOGGER.debug("resource_show: %s", res_data.text)

        resp_json = res_data.json()
        assert (not resp_json['success']) == conf_fixture.test_result


# post test cleanup removal of pkg if previous test fails. this is to be apart of the pre/post run at module level
# TODO: move this into a conftest
def test_post_cleanup(test_pkg_teardown):
    pkg = test_pkg_teardown
    LOGGER.debug('post cleanup: %s', pkg)
