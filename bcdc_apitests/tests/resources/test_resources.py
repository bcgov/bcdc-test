'''
Created on Jun. 11, 2019

@author: crigdon
'''

import logging
import requests
import ckanapi

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# TODO: Should have a method that cleans up in case the resource already exists
def test_resource_create(ckan_url, ckan_rest_dir, ckan_auth_header,
                         resource_data):
    '''
    add new resource

    :param ckan_url: domain to be used for ckan calls
    :param ckan_rest_dir: root path to the rest api
    :param ckan_auth_header: authorization header
    :param resource_data: the resource data to be used in the creation of a
        new resource object
    '''
    try:
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_create')
        logger.debug('api_call: %s', api_call)

        resp = requests.post(api_call, headers=ckan_auth_header, json=resource_data)
        logger.debug("resource_create: %s", resp.text)

        assert resp.status_code == 200
    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# update resource
def test_resource_update(remote_api_admin_auth, test_package_name, resource_data):
    remote_api = remote_api_admin_auth

    # using search to get the ID of resource.  needs to migrate as fixture via package query
    res_data = remote_api.action.resource_search(query="name:{0}".format(resource_data['name']))
    resId = res_data['results'][0]['id']

    logger.debug("resource_id: %s", resId)

    try:
        res_data = remote_api.action.resource_update(**resource_data)
        logger.debug("resource_update: %s", res_data)

    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# search resource
def test_resource_search(remote_api_admin_auth, resource_data):

    try:
        remote_api = remote_api_admin_auth

        # using search to get the ID of resource.  needs to migrate as fixture via package query
        res_data = remote_api.action.resource_search(query="name:{0}".format(resource_data['name']))
        logger.debug("resource_update: %s", res_data)

        res_id = res_data['results'][0]['id']
        logger.debug("resource_id: %s", res_id)
        assert res_data['count'] == 1
    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# delete resource
def test_resource_delete(remote_api_admin_auth, resource_data):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    '''
    try:

        remote_api = remote_api_admin_auth

        #res_data = remote_api.action.resource_search(query="name:test resource")
        #resId = res_data['results'][0]['id']
        #logger.debug("resource_id: %s", resId)

        resource_dict = {'name': resource_data['name']}
        res_data = remote_api.action.resource_delete(**resource_dict)
        logger.debug("resource_delete: %s", res_data)

        if res_data is None:
            pass
    except ckanapi.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)


# remove test package
def test_package_delete(ckan_url, ckan_auth_header,
                        ckan_rest_dir, test_package_name):
    '''
    verifies that a package can acutally be deleted
    '''
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_delete')
    logger.debug('api_call: %s', api_call)
    delete_data = {'id': test_package_name}

    resp = requests.post(api_call, headers=ckan_auth_header, json=delete_data)
    logger.debug('status code: %s', resp.status_code)
    resp_json = resp.json()
    logger.debug("resp: %s", resp.text)
    assert resp.status_code == 200
    assert resp_json['success']
