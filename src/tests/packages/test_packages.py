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
import pytest
from fixtures.load_config import ckan_restdir

logger = logging.getLogger(__name__)


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


def test_add_package_junk(test_pkg_data, ckan_url, ckan_apitoken):
    '''
    - checks to see if the package exists, removes if thats the case
    - adds the package
    - removes the package


    5-29-2019:
        - Thinking should do this using requests possibly as
          requests will allow finer graned evaluation of results
          from a api call.
        CREATE
               will pass on the work of adding a package to the
               fixtures.  All we are interested in is that an
               error was not thrown, and that after creating
               the package I can successfully retrieve it.

        READ
               can it be viewed in various methods that return the
               package data, search, list, show etc.

        DELETE
               can package be deleted.
    '''
    # ----------------------------------------------------------------
    # SETUP - make sure package doesn't exist
    # ----------------------------------------------------------------
    # think about moving logic code into fixtures then only assert the
    # results in the test code.  then can put teardown into the fixtures
    # as oppose to having it here.
    pkg_name = test_pkg_data['name']
    logger.debug("pkgName: %s", pkg_name)
    logger.debug("apitoken: %s", '*' * len(ckan_apitoken))

    remote_api = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
    pkg_list = remote_api.action.package_list()
    remote_api.action.package_delete(id=pkg_name)
    # this might go into the startup for pkg tests
    # need to use package_show to determine if object already exists.
    if pkg_name in pkg_list:
        # remove so can be re-added
        # could also add this to a wrapper fixture that gets called
        # at start and end of everything here.  Leaving it here for
        # now
        logger.debug("cleaning up package: %s", pkg_name)

    logger.debug("adding the package: %s", pkg_name)

    # CREATE THE PACKAGE
    pkg_created = False
    try:
        logger.debug("Adding package: %s", pkg_name)
        pkg_create = remote_api.action.package_create(**test_pkg_data)
        logger.debug("return value: %s", pkg_create)
        pkg_created = True
    except ckanapi.errors.ValidationError as err:
        logger.error("error: %s, %s", err, type(err))
        msg = 'Unable to create the package due to validation error, likely' + \
              ' already exists.  package name: {0}'
        msg = msg.format(pkg_name)
        # pytest.fail(msg, err)
        logger.debug(msg)
    assert pkg_created

    # VERIFY IT EXISTS
    # assert that the package exists
    # if the package doesn't exist package_show will raise an error
    pkg_data = None
    try:
        pkg_data = remote_api.action.package_show(id=pkg_name)
        logger.debug("package show: %s", pkg_data)
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)
    assert pkg_data
    logger.debug("finished adding record")

    # CLEANUP
    logger.debug("removing package...")
    remote_api.action.package_delete(id=pkg_name)
    logger.debug("package removed!")


def test_verify_package_count(ckan_url):
    '''
    verify the count reported by package_search matches packages
    returned by package_list
    '''
    # verify that the pkg_search and package_list report the same
    # total number of packages
    remote_api = ckanapi.RemoteCKAN(ckan_url)
    pkg_list = remote_api.action.package_list()
    pkg_search = remote_api.action.package_search()
    assert pkg_search['count'] == len(pkg_list)

