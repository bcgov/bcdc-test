'''
Created on Jun. 11, 2019

@author: crigdon
'''
import json
import logging

import requests

import bcdc_apitests.config.testConfig as testConfig

# pylint: disable=invalid-name,unused-argument, logging-fstring-interpolation
LOGGER = logging.getLogger(__name__)


def test_resource_create(conf_fixture, ckan_url, ckan_rest_dir, ckan_auth_header,
                         package_create_if_not_exists, resource_delete_if_exists,
                         bcdc_resource_populator,
                         remote_api_super_admin_auth):
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
    # need the package id
    pkg = remote_api_super_admin_auth.action.package_show(id=testConfig.TEST_PACKAGE)
    LOGGER.debug(f"package is: {pkg}")

    # conf_fixture contains the name of the 'bcdc_resource_populator' method that we
    # want to call to retrieve the required data,  These lines convert the name
    # of the method (in string) to an actual function reference (func)

    LOGGER.debug(f'conf_fixture dataname: {conf_fixture.test_data }')
    func = getattr(bcdc_resource_populator, conf_fixture.test_data[0])
    overrides = {'name': testConfig.TEST_RESOURCE,
                 'package_id': pkg['id']
                 }

    populate_bcdc_resource = func(overrides)

    # define api call
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_create')
    LOGGER.debug('api_call: %s', api_call)

    cnt = 1
    for resource_data in populate_bcdc_resource:
        resource_data['name'] = f'{testConfig.TEST_RESOURCE}_{cnt}'
        LOGGER.debug(f'resource data: {json.dumps(resource_data)}')

        # fix the json_table_schema
        if 'json_table_schema' in resource_data:
            LOGGER.debug(f"json_table_schema: {resource_data['json_table_schema']}")
            LOGGER.debug(f"json_table_schema type {type(resource_data['json_table_schema'])}")
            resource_data['json_table_schema'] = json.loads(resource_data['json_table_schema'])

        # create resource
        LOGGER.debug(f"api_call: {api_call}")
        res_data = requests.post(api_call, headers=ckan_auth_header, json=resource_data)
        LOGGER.debug("resource_create: %s", res_data.text)

        # get resource id
        LOGGER.debug('res_data.status_code: %s', res_data.status_code)
        resp_json = res_data.json()
        LOGGER.debug('resp_json: %s', resp_json)
        test_status = res_data.status_code == 200
        LOGGER.debug("test status: %s", test_status)
        assert_msg = f'status_code: {res_data.status_code}, text from bcdc: {resp_json}'
        assert test_status == conf_fixture.test_result, assert_msg
        if test_status:
            # if the we can successfully create the resource then make sure that
            # it shows up in a package_show
            # check is resource exist and shows up in resource_show
            # define remote api
            api_call_status = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_show')
            res_id = resp_json['result']['id']
            res_data = requests.get(api_call_status, headers=ckan_auth_header,
                                    params={'id':res_id})
            resp_json = res_data.json()
            assert resp_json['success'] == conf_fixture.test_result
        cnt += 1


# update resource
def test_resource_update(conf_fixture, ckan_url, ckan_rest_dir,
                         ckan_auth_header,
                         resource_get_id_fixture, populate_resource_single):
    '''
    :param conf_fixture: a test parameters object, contains all the properties
        of any parameterized tests.
    :type conf_fixture: helpers.read_test_config.TestParameters
    :param ckan_url: the ckan url to be used for the test
    :param ckan_rest_dir: the ckan rest dir to use for the test
    :param ckan_auth_header: auth header with api token configured for the
        parameterized user
    :param resource_data: test resource structure, this fixture will also make
        sure that a test package exists that it can use for the testing, and
        populates the package_id property in this object.
    :param resource_get_id_fixture:
    '''
    # to make it unique each time a parameterized run takes place appending
    # test id to the description
    updated_resource_description = 'test resource_update ({0})'.format(
        conf_fixture.get_as_id())

    # update resource data dic with resource id
    populate_resource_single['id'] = resource_get_id_fixture
    LOGGER.debug("resource_id: %s", populate_resource_single['id'])

    # change some data in resource data dic
    populate_resource_single['description'] = updated_resource_description

    # define api
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'resource_update')
    LOGGER.debug('api_call: %s', api_call)

    # update resource
    resp = requests.post(api_call, headers=ckan_auth_header, json=populate_resource_single)
    res_data = resp.json()
    LOGGER.debug("resource_update: %s", res_data)
    assert (resp.status_code == 200) == conf_fixture.test_result
    # the assuming returned 200 should make sure we can retrieve the changed
    # data
    if resp.status_code == 200 and res_data['success']:
        res_data = res_data['result']
        res_id = res_data['id']

        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_show')
        params = {'id': populate_resource_single['package_id']}
        resp = requests.post(api_call, headers=ckan_auth_header, params=params)
        resp_data = resp.json()
        assert (resp.status_code == 200 and resp_data['success']) == conf_fixture.test_result
        pckg = resp_data['result']
        LOGGER.debug('package has resources: %s'  'resources' in pckg)

        LOGGER.debug('package : %s', pckg)
        # make sure the package has at least one resource
        LOGGER.debug('resources is true: %s', (pckg['resources']))
        # doing it like this to force conversion to boolean
        assert (not pckg['resources']) != conf_fixture.test_result

        # verify that the resource is part of the package and retrieve that
        # specific resource...
        rsrc_exists = False
        cur_resrc = None
        for rsrc in pckg['resources']:
            if rsrc['id'] == res_id:
                rsrc_exists = True
                cur_resrc = rsrc
                break
        assert rsrc_exists == conf_fixture.test_result
        if rsrc_exists:
            assert (cur_resrc['description'] == updated_resource_description) == \
                conf_fixture.test_result


# search resource
def test_resource_search(conf_fixture, remote_api_auth, test_resource_name,
                         resource_get_id_fixture):
    '''
    :param remote_api_admin_auth: ckanapi remote, with auth
    :param test_resource_name: test resource name
    :param resource_get_id_fixture: This will ensure that the resource and all
        dependent objects are in existence prior to running this test.
    '''
    # define remote api
    remote_api = remote_api_auth

    # search for resource by name
    res_data = remote_api.action.resource_search(query="name:{0}".format(
        test_resource_name))
    LOGGER.debug("resource search results: %s", res_data)
    # assert the show turned up the same resource as was created
    LOGGER.debug("id expected: %s", resource_get_id_fixture)

    assert (res_data['count'] >= 1) == conf_fixture.test_result

    # getting all the different resource ids associated with the resource
    # search
    ids = []
    for res in res_data['results']:
        ids.append(res['id'])
    # verify that the expected resource id is included in the returned values
    # from the search
    assert (resource_get_id_fixture in ids) == conf_fixture.test_result


# delete resource
def test_resource_delete(conf_fixture, ckan_url,
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
    # define api
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

        # show resource, to later verify that the id cannot be found
        res_data = requests.get(api_call, headers=ckan_auth_header,
                                params={'id': resource_get_id_fixture})
        LOGGER.debug("resource_show: %s", res_data.text)

        resp_json = res_data.json()
        assert (not resp_json['success']) == conf_fixture.test_result
