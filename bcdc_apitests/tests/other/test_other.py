'''

Created on Sep 09, 2019

@author: crigdon

contains test that are not related to a existing test module

'''
# pylint: disable=invalid-name, unused-argument, too-many-arguments, unused-import
import logging
import requests
import pytest  # @UnusedImport

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name



def test_dashboard_activity_list(conf_fixture, user_label_fixture, remote_api_auth, test_pkg_data, test_package_name,
                                 ckan_url, ckan_rest_dir, ckan_auth_header, package_delete_if_exists, test_pkg_teardown):
    '''
    :param remote_api_auth: a ckan remote api object
    :param test_pkg_data: pkg data to be updated
    :param test_package_name: the package name that is to be deleted if it
                      exists.
    :param user_label_fixture: get user name

    Create pkg and then check if pkg_id is recorded in the activity_list as an object_id
    '''


    # create new pkg as user
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_create')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.post(api_call, headers=ckan_auth_header, json=test_pkg_data)
    assert (resp.status_code == 200) == conf_fixture.test_result
    pkg_data = resp.json()
    new_pkg_id = pkg_data['result']['id']
    LOGGER.debug('new_pkg_id: %s', new_pkg_id)

    # get activity list
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'dashboard_activity_list')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.post(api_call, headers=ckan_auth_header)
    assert (resp.status_code == 200) == conf_fixture.test_result
    activity_data = resp.json()

    # check if newly created pkg is in activity list
    activity_found = False
    for activity in activity_data['result']:
        LOGGER.debug('object_id: %s', activity['object_id'])
        if new_pkg_id == activity['object_id']:
            revision_id = activity['object_id']
            LOGGER.debug('object_id: %s', revision_id)
            activity_found = True

    fail_msg = "did not find the activity in user_activity_list when " + \
        "retrieved as {0}"
    fail_msg = fail_msg.format(user_label_fixture)
    assert activity_found == conf_fixture.test_result, fail_msg





def test_tag_list(conf_fixture):
    '''
    :param remote_api: a ckan remote api object
    :param pkg_name:  the package name that is to be deleted if it
                      exists.
    '''

def test_vocabulary_list(conf_fixture):
    '''
    :param remote_api: a ckan remote api object
    :param pkg_name:  the package name that is to be deleted if it
                      exists.
    '''

def test_license_list(conf_fixture):
    '''
    :param remote_api: a ckan remote api object
    :param pkg_name:  the package name that is to be deleted if it
                      exists.
    '''

def test_config_option_show(conf_fixture):
    '''
    :param remote_api: a ckan remote api object
    :param pkg_name:  the package name that is to be deleted if it
                      exists.
    '''

