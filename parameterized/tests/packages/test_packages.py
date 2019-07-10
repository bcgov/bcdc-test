'''
Created on May 15, 2019

@author: KJNETHER

used to verify ability to create packages:

a) create org, retrieve id
    - do round crud test or org.
b) create package with org insert the org just created for this package.

'''

import logging

import ckanapi
import pytest
import requests
import inspect

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# def test_add_package_success(conf_fixture, user_label_fixture, data_label_fixture):
#     #print 'ckan_auth_header', ckan_auth_header
#     #print 'got here ', ckan_auth_header
#     # need to figure out how to retrieve expected results.
#     # below shows how we could get the module, name and function
#     # the use the helper.read_test_config to get the expected results
#     #  thinking need to go back to breaking up the testParams.json into 
#     #  an individual test per record.
#     print 'current file', __file__
#     print 'conf_fixture', conf_fixture
#     print 'user', user_label_fixture
#     print 'data', data_label_fixture
#     print 'expectations', conf_fixture.test_result


def test_add_package_success(conf_fixture, ckan_auth_header, test_pkg_data, expected, 
                             test_pkg_teardown, ckan_url, ckan_rest_dir):
    '''
    makes simple request to create package and verifies it gets
    200 status code.
 
    Using requests to form this call to get status code and for increased level
    of granularity over
    '''
    #ckan_auth_header = get_package_test_data[0]
    #test_pkg_data = get_package_test_data[1]
    #expected = get_package_test_data[2]
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_create')
    logger.debug('api_call: %s', api_call)
 
    resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    logger.debug("resp: %s", resp.text)
    logger.info("status code: %s", resp.status_code)
    #assert resp.status_code == 200
    assert resp.ok == expected





def test_view_package(conf_fixture, ckan_auth_header2):
    print 'hello'
    print 'conf_fixture', conf_fixture, type(conf_fixture)
    print 'auth header: ', ckan_auth_header2
    

