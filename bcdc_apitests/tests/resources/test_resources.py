'''
Created on Jun. 11, 2019

@author: crigdon
'''

import logging
import requests
import ckanapi


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def test_resource_create(ckan_url, ckan_rest_dir, ckan_auth_header,
                         resource_data, package_create_if_not_exists):
    '''
    add new resource

    :param ckan_url: domain to be used for ckan calls
    :param ckan_rest_dir: root path to the rest api
    :param ckan_auth_header: authorization header
    :param resource_data: the resource data to be used in the creation of a
        new resource object
    :param package_create_if_not_exists: create pkg if it does not exist
    '''

    pkg = package_create_if_not_exists
    logger.debug("package_create id is: %s", pkg['id'])

    try:
        # define api call
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_create')
        logger.debug('api_call: %s', api_call)

        # get pkg id
        resource_data['package_id'] = pkg['id']

        # create resource
        res_data = requests.post(api_call, headers=ckan_auth_header, json=resource_data)
        logger.debug("resource_create: %s", res_data.text)

        # get resource id
        resp_json = res_data.json()
        resId = resp_json['result']['id']

        assert res_data.status_code == 200

        # check is resource exist
        # define remote api
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_show')
        logger.debug('api_call: %s', api_call)
        res_data = requests.post(api_call, headers=ckan_auth_header, json={'id': resId})
        logger.debug("resource_show: %s", res_data.text)

        resp_json = res_data.json()

        assert resp_json['success']

    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)
        raise err


# update resource
def test_resource_update(ckan_url, ckan_rest_dir, ckan_auth_header, resource_data,
                         package_get_id_fixture, resource_get_id_fixture):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    :param resource_data: test resource structure
    :param ckan_url:
    :param ckan_rest_dir:
    :param ckan_auth_header:
    :param package_get_id:
    :param resource_get_id_fixture:
    '''
    try:

        # update resource data dic with package id
        resource_data['package_id'] = package_get_id_fixture
        logger.debug("resource_pkgID: %s", resource_data['package_id'])

        # update resource data dic with resource id
        resource_data['id'] = resource_get_id_fixture
        logger.debug("resource_id: %s", resource_data['id'])

        # change some data in resource data dic
        resource_data['description'] = 'test resource description changed'

        # define api
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_update')
        logger.debug('api_call: %s', api_call)

        # update resource
        res_data = requests.post(api_call, headers=ckan_auth_header, json=resource_data)
        logger.debug("resource_update: %s", res_data.text)

        assert res_data.status_code == 200

    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# search resource
def test_resource_search(remote_api_admin_auth, test_resource_name):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    :param test_resource_name: test resource name
    '''
    try:
        # define remote api
        remote_api = remote_api_admin_auth

        # search for resource by name
        res_data = remote_api.action.resource_search(query="name:{0}".format(test_resource_name))
        logger.debug("resource search results: %s", res_data)

        assert res_data['count'] >= 1

    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# delete resource
def test_resource_delete(remote_api_admin_auth, ckan_url, ckan_rest_dir, ckan_auth_header, resource_get_id_fixture):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    :param resource_data: test resource structure
    :param ckan_url:
    :param ckan_rest_dir:
    :param ckan_auth_header:
    :param resource_get_id_fixture:
    '''
    try:
        # define api
        remote_api = remote_api_admin_auth

        # delete resource by id
        res_data = remote_api.action.resource_delete(id=resource_get_id_fixture)
        logger.debug("resource_delete: %s", res_data)

        # check is resource exist
        # define api
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_show')
        logger.debug('api_call: %s', api_call)

        # show resource
        res_data = requests.post(api_call, headers=ckan_auth_header, json={'id': resource_get_id_fixture})
        logger.debug("resource_show: %s", res_data.text)

        resp_json = res_data.json()
        assert not resp_json['success']

    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# post test cleanup removal of pkg if previous test fails. this is to be apart of the pre/post run at module level
# TODO: move this into a conftest
def test_post_cleanup(test_pkg_teardown):
    pkg = test_pkg_teardown
    logger.debug('post cleanup: %s', pkg)