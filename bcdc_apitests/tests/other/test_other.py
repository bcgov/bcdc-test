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

@pytest.mark.xfail
def test_dashboard_activity_list(conf_fixture, user_label_fixture,
                                 remote_api_auth, populate_bcdc_dataset_single,
                                 test_package_name, ckan_url, ckan_rest_dir,
                                 ckan_auth_header, package_delete_if_exists,
                                 test_pkg_teardown):
    '''
    :param remote_api_auth: a ckan remote api object
    :param populate_bcdc_dataset: pkg data to be updated
    :param test_package_name: the package name that is to be deleted if it
                      exists.
    :param user_label_fixture: get user name

    Create pkg and then check if pkg_id is recorded in the activity_list as an object_id for that user
    '''

    # create new pkg as user
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_create')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.post(api_call, headers=ckan_auth_header,
                         json=populate_bcdc_dataset_single)
    assert (resp.status_code == 200) == conf_fixture.test_result
    pkg_data = resp.json()
    new_pkg_id = pkg_data['result']['id']
    LOGGER.debug('new_pkg_id: %s', new_pkg_id)

    # get activity list
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir,
                                   'dashboard_activity_list')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.post(api_call, headers=ckan_auth_header)
    assert (resp.status_code == 200) == conf_fixture.test_result
    activity_data = resp.json()

    # check if newly created pkg is in activity list
    activity_found = False
    for activity in activity_data['result']:
        # LOGGER.debug('object_id: %s', activity['object_id'])
        if new_pkg_id == activity['object_id']:
            revision_id = activity['object_id']
            LOGGER.debug('found object_id: %s', revision_id)
            activity_found = True

    fail_msg = "did not find the activity in user_activity_list when " + \
        "retrieved as {0}"
    fail_msg = fail_msg.format(user_label_fixture)
    assert activity_found == conf_fixture.test_result, fail_msg


def test_tag_list(conf_fixture, remote_api_auth, package_create_if_not_exists,
                user_label_fixture, test_package_name, ckan_url, ckan_rest_dir, ckan_auth_header,
                ckan_superadmin_auth_header):
    '''
    :param remote_api: a ckan remote api object

    ckan idiosyncrasy #101: tag_list returns non vocab tags,
    as tag_create creates vocab tags, so makes since to use
    package_update to create new non vocab tags. concluding..
    to delete non vocab tag use tag_delete,
    and use vocabulary_delete to delete your tag vocabulary.


    test will get a tag from test pkg and check if it is return by list that is returned by user.
    future test could create tag then check if returned by list api.
    '''

    # get pkg tags from test pkg
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'package_show')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_superadmin_auth_header, params={'id': test_package_name})
    assert (resp.status_code == 200) == conf_fixture.test_result
    pkg_data = resp.json()

    pkg_tag = pkg_data['result']['tags'][0]
    LOGGER.debug("pkg_tag: %s", pkg_tag)

    # get tag list
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'tag_list')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.post(api_call, headers=ckan_superadmin_auth_header)
    assert (resp.status_code == 200) == conf_fixture.test_result
    tag_list_data = resp.json()

    # check if tag is in tag list
    tag_found = False
    for tag in tag_list_data['result']:
        LOGGER.debug('tag_list: %s', tag)
        if pkg_tag['name'] == tag:
            LOGGER.debug('tag_found: %s', pkg_tag['name'])
            tag_found = True

    fail_msg = "did not find the tag in tag_list when " + \
        "retrieved as {0}"
    fail_msg = fail_msg.format(user_label_fixture)
    assert tag_found == conf_fixture.test_result, fail_msg


def test_vocabulary_list(conf_fixture, remote_api_super_admin_auth):
    '''
    :param remote_api: a ckan remote api object
    :param remote_api_super_admin_auth: a ckan remote api auth token for sysAdmin

    must run as sysAdmin
    get list of vocabularies and check count if >= 1
    Future update could use tag_create to creates vocab tags and then check if exist in list.
    '''

    # get list of license
    vocabulary_list_data = remote_api_super_admin_auth.action.vocabulary_list()
    vocab_count = len(vocabulary_list_data)
    LOGGER.debug("vocab_count: %s", vocab_count)
    fail_msg = "failed to get vocabulary list option with count {0}"
    fail_msg = fail_msg.format(vocab_count)

    # check count
    returned_count = vocab_count >= 1
    assert returned_count == conf_fixture.test_result, fail_msg


def test_license_list(conf_fixture, user_label_fixture, remote_api_auth):
    '''
    :param remote_api: a ckan remote api object
    :param user_label_fixture: user name
    :param remote_api_auth: a ckan remote api auth token

    get list of license and check count if >= 1
    '''

    # get list of license
    license_list_data = remote_api_auth.action.license_list()
    license_count = len(license_list_data)
    LOGGER.debug("license_count: %s", license_count)
    fail_msg = "failed to get licence list option for {0}  with count {1}"
    fail_msg = fail_msg.format(user_label_fixture, license_count)

    # check count
    returned_count = license_count >= 1
    assert returned_count == conf_fixture.test_result, fail_msg


def test_config_option_show(conf_fixture, remote_api_super_admin_auth,
                            ckan_url, ckan_rest_dir, ckan_superadmin_auth_header):
    '''
    :param remote_api: a ckan remote api object

    sysAdmin Only
    get list of all config options and check if each option can be retrieved with success
    '''

    # get list of all available config options
    config_option_list_data = remote_api_super_admin_auth.action.config_option_list()
    LOGGER.debug("config_option_list_data: %s", config_option_list_data)

    # get config option for all options in list and check each for success
    for config in config_option_list_data:
        api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'config_option_show')
        LOGGER.debug('api_call: %s', api_call)
        resp = requests.post(api_call, headers=ckan_superadmin_auth_header, params=
                        {'key': config})
        # check for 200
        fail_msg = "failed to get config data option for {0}  with status {1}"
        fail_msg = fail_msg.format(config, resp.status_code)
        assert (resp.status_code == 200) == conf_fixture.test_result, fail_msg

        # check if success = True
        config_option_show_data = resp.json()
        LOGGER.debug("config_option_show_data: %s", config_option_show_data)
        fail_msg = "failed to get config data option for {0} "
        fail_msg = fail_msg.format(config)
        assert config_option_show_data['success'] == conf_fixture.test_result, fail_msg

