'''
Created on May 15, 2019

@author: KJNETHER

used to verify ability to create packages:

a) create org, retrieve id
    - do round crud test or org.
b) create package with org insert the org just created for this package.

'''

import inspect
import logging
import time

import ckanapi
import pytest  # @UnusedImport
import requests

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name

# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument


def test_package_create(conf_fixture, ckan_auth_header, test_pkg_data,
                        test_pkg_teardown, package_delete_if_exists, ckan_url,
                        ckan_rest_dir):

    '''
    makes simple request to create package and verifies it gets
    200 status code.

    Using requests to form this call to get status code and for increased level
    of granularity over
    '''
    # debugging the parameterization, makes sure this test is getting the correct
    # parameters
    func_name = inspect.stack()[0][3]
    LOGGER.debug("func_name %s, %s", func_name, conf_fixture.test_function)
    if func_name != conf_fixture.test_function:
        raise ValueError("incorrect conf_fixtures was sent")

    LOGGER.debug("conf_fixture: expected %s", conf_fixture.test_result)
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_create')
    LOGGER.debug('api_call: %s', api_call)
    LOGGER.debug('ckan_auth_header: %s', ckan_auth_header)
    LOGGER.debug('test_pkg_data: %s', test_pkg_data)
    resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    if resp.status_code == 502:
        # try again
        time.sleep(3)
        LOGGER.debug('api_call: %s', ckan_auth_header)
        LOGGER.debug('api_call: %s', test_pkg_data)
        resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    LOGGER.debug("resp: %s", resp.text)
    LOGGER.info("status code: %s", resp.status_code)
    assert (resp.status_code == 200) == conf_fixture.test_result


def test_package_show(conf_fixture, remote_api_auth, test_package_name,
                      package_create_if_not_exists):
    '''
    verify package data can be retrieved using package_show.

    :param param: remote_api_admin_auth
    '''
    # debugging the parameterization, makes sure this test is getting the correct
    # parameters
    func_name = inspect.stack()[0][3]
    LOGGER.debug("func_name %s, %s", func_name, conf_fixture.test_function)
    if func_name != conf_fixture.test_function:
        raise ValueError("incorrect conf_fixtures was sent")

    LOGGER.debug("conf_fixture: expected %s", conf_fixture.test_result)
    LOGGER.debug("conf_fixture:  %s", conf_fixture)
    # should this be a requests call instead of ckanapi?
    pkg_show_data = remote_api_auth.action.package_show(id=test_package_name)
    LOGGER.debug("pkg_show_data: %s", pkg_show_data)
    LOGGER.debug("package name: %s", pkg_show_data['name'])
    LOGGER.debug("expected name: %s", test_package_name)
    LOGGER.debug("expected outcome: %s", conf_fixture.test_result)
    assert (pkg_show_data['name'] == test_package_name) == conf_fixture.test_result

def test_package_state(remote_api_admin_auth, update_pkg_state, test_package_name):
    '''
    verify package data can be retrieved using package_show.

    :param param: remote_api_admin_auth
    '''

    pkg_show_data = remote_api_admin_auth.action.package_show(id=test_package_name)
    logger.debug("pkg_show_data: %s", pkg_show_data)

    assert pkg_show_data['name'] == test_package_name


def test_package_visibility(remote_api_admin_auth, update_pkg_visibility, test_package_name):
    '''
    verify package data can be retrieved using package_show.

    :param param: remote_api_admin_auth
    '''

    pkg_show_data = remote_api_admin_auth.action.package_show(id=test_package_name)
    logger.debug("pkg_show_data: %s", pkg_show_data)

    assert pkg_show_data['name'] == test_package_name



def test_package_update(conf_fixture, remote_api_auth, test_pkg_data, ckan_url,
                        ckan_rest_dir, ckan_auth_header,
                        package_create_if_not_exists, test_pkg_teardown):
    '''
    package update test will use requests
    :param conf_fixture: a test parameters object that wraps the records
                         described in test_data.testParams.json.
    :type conf_fixture: helpers.read_test_config.TestParameters
    :param remote_api_auth: a ckanapi remote object with auth
    :param test_pkg_data: the package data
    :param ckan_url: ckan domain
    :param ckan_rest_dir: path to rest dir
    :param ckan_auth_header: authorization header to use in request, changes
                             based on the different users that will use the
                             test
    :param package_create_if_not_exists: this test needs the test package to
                        exist when its running.  Creates it if it does not
                        already exist
    '''
    # debugging the parameterization, makes sure this test is getting the correct
    # parameters
    func_name = inspect.stack()[0][3]
    LOGGER.debug("func_name %s, %s", func_name, conf_fixture.test_function)
    if func_name != conf_fixture.test_function:
        raise ValueError("incorrect conf_fixtures was sent")

    test_package_name = test_pkg_data['name']
    original_title = test_pkg_data['title']
    test_pkg_data['title'] = 'zzz changed the title'
    pkg_show_data_orig = remote_api_auth.action.package_show(id=test_package_name)
    # LOGGER.debug("pkg_show_data: %s", pkg_show_data)

    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_update')
    resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    LOGGER.debug("resp.status_code: %s", resp.status_code)
    LOGGER.debug("resp.status_code: %s", resp.text)
    assert (resp.status_code == 200) == conf_fixture.test_result
    # now double check that the data has been changed
    pkg_show_data = remote_api_auth.action.package_show(id=test_package_name)
    assert (pkg_show_data['title'] == test_pkg_data['title']) == conf_fixture.test_result
    assert (pkg_show_data_orig['title'] != pkg_show_data['title']) == conf_fixture.test_result

    # now change back to original values so test will work on next iteration,
    # but also alows further testing of the package_update
    # only run if the data was successfully changed.
    if pkg_show_data['title'] == test_pkg_data['title']:
        test_pkg_data['title'] = original_title
        resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
        assert (resp.status_code == 200) == conf_fixture.test_result
        pkg_show_data = remote_api_auth.action.package_show(id=test_package_name)
        assert (pkg_show_data['title'] == original_title) == conf_fixture.test_result


@pytest.mark.xfail
def test_package_list_vs_package_show(conf_fixture,  # pylint: disable=invalid-name, too-many-arguments
                                      ckan_url,
                                      ckan_rest_dir,
                                      ckan_auth_header,
                                      package_create_if_not_exists):
    '''
    verify the count reported by package_search matches packages
    returned by package_list, als seeing as a package has been
    added it should be 1 or more

    :param ckan_url: the domain portion of the ckan path
    :param ckan_rest_dir: directory path to rest calls
    :param ckan_auth_header: header struct with auth token
    '''
    # debugging the parameterization, makes sure this test is getting the correct
    # parameters
    func_name = inspect.stack()[0][3]
    LOGGER.debug("func_name %s, %s", func_name, conf_fixture.test_function)
    if func_name != conf_fixture.test_function:
        raise ValueError("incorrect conf_fixtures was sent")

    # using requests as can't get the limit to work with ckanapi.
    package_list_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_list')
    params = {'limit': 500, 'offset': 0}
    package_list_cnt = 0
    while True:
        LOGGER.debug("offset: %s", params['offset'])
        resp = requests.get(package_list_call, headers=ckan_auth_header,
                            params=params)
        LOGGER.debug("status: %s", resp.status_code)
        pkg_list = resp.json()
        package_list_cnt = package_list_cnt + len(pkg_list['result'])
        LOGGER.debug("package cnt: %s %s", package_list_cnt,
                     len(pkg_list['result']))
        if len(pkg_list['result']) < params['limit']:
            LOGGER.debug("end of pages, breaking out")
            break
        params['offset'] = params['limit'] + params['offset']

    LOGGER.debug("final package cnt from packagelist: %s", package_list_cnt)

    remote_api = ckanapi.RemoteCKAN(ckan_url)
    pkg_search = remote_api.action.package_search()

    LOGGER.debug("pkg_search cnt: %s", pkg_search['count'])
    LOGGER.debug("pkglist cnt: %s", package_list_cnt)
    assert (pkg_search['count'] == package_list_cnt) == conf_fixture.test_result
    assert (len(pkg_list) >= 1) == conf_fixture.test_result


def test_package_delete(conf_fixture, ckan_url,  # pylint: disable=invalid-name
                        ckan_auth_header, ckan_rest_dir, test_package_name,
                        package_create_if_not_exists):
    '''
    verifies that a package can actually be deleted,

     - removed the purge calls because purge is completed by superadmin
       no by the test user.
    '''
    # debugging the parameterization, makes sure this test is getting the correct
    # parameters
    func_name = inspect.stack()[0][3]
    LOGGER.debug("func_name %s, %s", func_name, conf_fixture.test_function)
    if func_name != conf_fixture.test_function:
        raise ValueError("incorrect conf_fixtures was sent")

    # delete pkg
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_delete')
    LOGGER.debug('api_call: %s', api_call)
    delete_data = {'id': test_package_name}

    resp = requests.post(api_call, headers=ckan_auth_header, json=delete_data)
    LOGGER.debug('status code: %s', resp.status_code)
    resp_json = resp.json()
    LOGGER.debug("resp: %s", resp.text)
    LOGGER.debug("resp_json['success'] type(): %s, %s, %s", type(resp_json['success']),
                 resp_json['success'], conf_fixture.test_result)
    assert (resp.status_code == 200) == conf_fixture.test_result
    assert resp_json['success'] == conf_fixture.test_result


# its known that this test will currently fail.  remove this decorator once this
# issue is patched
@pytest.mark.xfail
def test_create_package_coredataonly(conf_fixture, ckan_url,  # pylint: disable=invalid-name
                                     ckan_auth_header, ckan_rest_dir,
                                     test_pkg_data_core_only,
                                     package_delete_if_exists):
    '''
    CKAN Documentation suggests these are the core attributes required for a
    package:
        - name (string)
        - title (string)
        - private (bool)
        - owner_org (configurable as optional, assuming its not)

    This tests asserts that creating a package using these core attributes does
    not result in a "ghost package"

    ghost package: package_create returns 200, but subsequent package_shows
                   on same package return 500
    :param test_pkg_teardown: This fixture returns a teardown method that can be
            called multiple times to clean up package data created by this test
    :param ckan_url: url to use in construction of api calls
    :param ckan_auth_header: the auth header to use in api calls
    :param ckan_rest_dir: the directory to the api
    :param test_pkg_data_core_only: data structure that represents a test package
            that can be used in this test

    using pytest_check to provide delayed assertion
    '''
    # debugging the parameterization, makes sure this test is getting the correct
    # parameters
    func_name = inspect.stack()[0][3]
    LOGGER.debug("func_name %s, %s", func_name, conf_fixture.test_function)
    if func_name != conf_fixture.test_function:
        raise ValueError("incorrect conf_fixtures was sent")

    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_create')
    LOGGER.debug('api_call: %s', api_call)

    resp_create = requests.post(api_call, headers=ckan_auth_header,
                                json=test_pkg_data_core_only)
    LOGGER.debug("resp: %s", resp_create.text)
    cant_create_msg = 'Attempt to call %s returned %s'
    cant_create_msg = cant_create_msg.format(api_call,
                                             resp_create.status_code)
    # core data only create is successful.
    assert (resp_create.status_code != 200) == conf_fixture.test_result, \
        cant_create_msg

    # now make sure the data is viewable
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_show')
    LOGGER.debug('api_call: %s', api_call)
    resp_show = requests.post(api_call, headers=ckan_auth_header,
                              json={'id': test_pkg_data_core_only['name']})
    LOGGER.debug('resp: %s', resp_show.text)
    non_200_msg = 'package_show on package {0} returned a status_code {1} when ' + \
                  'package_create reported {2}'

    non_200_msg = non_200_msg.format(test_pkg_data_core_only['name'],
                                     resp_show.status_code,
                                     non_200_msg)

    # core only data is successful in viewing
    assert (resp_show.status_code == 200) == resp_create.status_code, \
        non_200_msg

    LOGGER.debug("resp text: %s", resp_show.text)
    LOGGER.debug("tear down has been called")
