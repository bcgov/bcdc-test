'''
Created on Jun. 11, 2019

@author: crigdon
'''


import logging
import requests
import ckanapi

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# create test package
def test_package_create(package_create_fixture):
    print package_create_fixture


# add resource
def test_resource_create(test_data_dir,test_package_name,remote_api_admin_auth,ckan_url,ckan_rest_dir,ckan_auth_header):

    #csv test file to try later
    #resource = os.path.join(test_data_dir, 'resData.csv')

    resource_dict = {'package_id': test_package_name,
                     'url': "https://docs.ckan.org/en/2.8/_static/ckanlogo.png",
                     'file': "https://docs.ckan.org/en/2.8/_static/ckanlogo.png",
                     'resource_storage_location': "External",
                     "edc_resource_type": "Data",
                     "format": "html",
                     "type": "DATA",
                     "resource_update_cycle": "asNeeded",
                     "resource_storage_access_method": "Direct Access",
                     "name": "test resource",
                     "projection_name": "N-A",
                     "description": "test resource description"
                     }
    try:
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_create')
        logger.debug('api_call: %s', api_call)

        resp = requests.post(api_call, headers=ckan_auth_header, json=resource_dict)
        logger.debug("resource_create: %s", resp.text)



        assert resp.status_code == 200
    except ckanapi.errors as err:
        logger.debug("err: %s %s", type(err), err)


# update resource
def test_resource_update(remote_api_admin_auth,test_package_name):
    remote_api = remote_api_admin_auth

    #using search to get the ID of resource.  needs to migrate as fixture via package query
    res_data = remote_api.action.resource_search(query="name:test resource")
    resId = res_data['results'][0]['id']

    logger.debug("resource_id: %s", resId)

    resource_dict = {'id': resId,
                     'package_id': test_package_name,
                     'url': "https://docs.ckan.org/en/2.8/_static/ckanlogo.png",
                     'file': "https://docs.ckan.org/en/2.8/_static/ckanlogo.png",
                     'resource_storage_location': "External",
                     "edc_resource_type": "Data",
                     "format": "html",
                     "type": "DATA",
                     "resource_update_cycle": "asNeeded",
                     "resource_storage_access_method": "Direct Access",
                     "name": "test resource",
                     "projection_name": "N-A",
                     "description": "test resource description changed"
                     }
    try:
        res_data = remote_api.action.resource_update(**resource_dict)
        logger.debug("resource_update: %s", res_data)

    except ckanapi.errors as err:
        logger.debug("err: %s %s", type(err), err)


# search resource
def test_resource_search(remote_api_admin_auth):

    try:
        remote_api = remote_api_admin_auth
        #using search to get the ID of resource.  needs to migrate as fixture via package query
        res_data = remote_api.action.resource_search(query="name:test resource")
        logger.debug("resource_update: %s", res_data)

        resId= res_data['results'][0]['id']
        logger.debug("resource_id: %s", resId)
        assert res_data['count'] == 1
    except ckanapi.errors as err:
        logger.debug("err: %s %s", type(err), err)


# delete resource
def test_resource_delete(remote_api_admin_auth):

    try:

        remote_api = remote_api_admin_auth

        res_data = remote_api.action.resource_search(query="name:test resource")
        resId= res_data['results'][0]['id']
        logger.debug("resource_id: %s", resId)

        resource_dict = {'id': resId}
        res_data = remote_api.action.resource_delete(**resource_dict)
        logger.debug("resource_delete: %s", res_data)

        if res_data is None:
            pass
    except ckanapi.errors as err:
        logger.debug("err: %s %s", type(err), err)


#remove test package
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
