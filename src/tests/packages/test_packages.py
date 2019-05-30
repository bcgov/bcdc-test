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
import requests
import pytest  # @UnusedImport

logger = logging.getLogger(__name__)  #pylint: disable=invalid-name


def test_add_package_success(test_pkg_teardown, ckan_url, ckan_auth_header,
                             ckan_restdir, test_pkg_data):
    '''
    makes simple request to create package and verifies it gets
    200 status code.

    Using requests to form this call to get status code and for increased level
    of granularity over
    '''
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_restdir, 'package_create')
    logger.debug('api_call: %s', api_call)

    resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    logger.debug("resp: %s", resp.text)
    assert resp.status_code == 200


def test_package_show(remote_api_admin_auth, test_package_name):
    '''
    going to verify package data can be retrieved using package_show.
    '''
    pkg_show_data = remote_api_admin_auth.action.package_show(id=test_package_name)
    logger.debug("pkg_show_data: %s", pkg_show_data)
    assert pkg_show_data['name'] == test_package_name


def test_package_update(remote_api_admin_auth, test_pkg_data, ckan_url,
                        ckan_restdir, ckan_auth_header):
    '''
    package update test will use requests
    '''
    test_package_name = test_pkg_data['name']
    pkg_show_data = remote_api_admin_auth.action.package_show(id=test_package_name)
    logger.debug("pkg_show_data: %s", pkg_show_data)
    # now modify the package show data and update

    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_restdir, 'package_update')
    resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    logger.debug("resp: %s", resp.text)
    logger.debug("resp.status_code: %s", resp.status_code)
    assert resp.status_code == 200
    # now double check that the data has been changed
    pkg_show_data = remote_api_admin_auth.action.package_show(id=test_package_name)
    assert pkg_show_data['title'] == test_pkg_data['title']


def test_verify_package_count(ckan_url):
    '''
    verify the count reported by package_search matches packages
    returned by package_list, als seeing as a package has been
    added it should be 1 or more
    '''
    # verify that the pkg_search and package_list report the same
    # total number of packages
    remote_api = ckanapi.RemoteCKAN(ckan_url)
    pkg_list = remote_api.action.package_list()
    pkg_search = remote_api.action.package_search()
    assert pkg_search['count'] == len(pkg_list)
    assert len(pkg_list) >= 1


def test_package_delete(ckan_url, ckan_auth_header,
                        ckan_restdir, test_package_name):
    '''
    verifies that a package can acutally be deleted
    '''
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_restdir, 'package_delete')
    logger.debug('api_call: %s', api_call)
    delete_data = {'id': test_package_name}

    resp = requests.post(api_call, headers=ckan_auth_header, json=delete_data)
    resp_json = resp.json()
    logger.debug("resp: %s", resp.text)
    assert resp.status_code == 200
    assert resp_json['success']
