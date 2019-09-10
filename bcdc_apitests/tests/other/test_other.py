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


def test_tag_list(conf_fixture, remote_api_auth):
    '''
    :param remote_api: a ckan remote api object

    '''
    #TODO: WIP
    tag_list_data = remote_api_auth.action.tag_list()
    LOGGER.debug("tag_list_data: %s", tag_list_data)


def test_vocabulary_list(conf_fixture, remote_api_super_admin_auth):
    '''
    :param remote_api: a ckan remote api object

    sysAdmin Only
    '''
    #TODO: WIP
    vocabulary_list_data = remote_api_super_admin_auth.action.vocabulary_list()
    LOGGER.debug("vocabulary_list_data: %s", vocabulary_list_data)


def test_license_list(conf_fixture, remote_api_auth):
    '''
    :param remote_api: a ckan remote api object

    '''
    #TODO: WIP
    license_list_data = remote_api_auth.action.license_list()
    LOGGER.debug("license_list_data: %s", license_list_data)


def test_config_option_show(conf_fixture, remote_api_super_admin_auth,
                            ckan_url, ckan_rest_dir, ckan_superadmin_auth_header):
    '''
    :param remote_api: a ckan remote api object


    check if config options can be retrieved with success
    sysAdmin Only
    '''

    # get list of all available config options
    config_option_list_data = remote_api_super_admin_auth.action.config_option_list()
    LOGGER.debug("config_option_list_data: %s", config_option_list_data)

    # get config option for all options and check each if success
    for config in config_option_list_data:
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'config_option_show')
        LOGGER.debug('api_call: %s', api_call)
        resp = requests.post(api_call, headers=ckan_superadmin_auth_header, params=
                        {'key': config})
        fail_msg = "failed to get config data option for {0}  with status {1}"
        fail_msg = fail_msg.format(config, resp.status_code)
        assert (resp.status_code == 200) == conf_fixture.test_result, fail_msg

        config_option_show_data = resp.json()
        LOGGER.debug("config_option_show_data: %s", config_option_show_data)
        fail_msg = "failed to get config data option for {0} "
        fail_msg = fail_msg.format(config)
        assert config_option_show_data['success'] == conf_fixture.test_result, fail_msg



