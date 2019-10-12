'''

Created on Sept 05, 2019

@author: crigdon

'''
# pylint: disable=invalid-name, unused-argument, too-many-arguments, unused-import
import logging
import requests
import pytest  # @UnusedImport

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name


def test_group_list(conf_fixture, group_create_if_not_exists_fixture,
                    test_group, ckan_url, ckan_rest_dir,
                    ckan_auth_header, user_label_fixture):
    '''
    verifies can retrieve a list of groups and that there is at least
    one group defined
    '''
    # this should be a requests call to verify status
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'group_list')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_auth_header, params=
                        {'id': test_group})
    resp_data = resp.json()
    LOGGER.debug("resp json: %s", resp_data)

    # assert that was success and 200
    non_200_msg = 'called the end point group_list as {0} and returned ' + \
                  'status code: {1}'
    non_200_msg = non_200_msg.format(user_label_fixture, resp.status_code)
    assert resp.status_code == 200, non_200_msg

    success_msg = 'group_list called as {0} returned success {1}'
    success_msg = success_msg.format(user_label_fixture, conf_fixture.test_result)
    assert resp_data['success'] == conf_fixture.test_result, success_msg

    group_list = resp_data['result']
    LOGGER.debug("group_list: %s", group_list)
    LOGGER.debug("group_list cnt: %s", len(group_list))
    group_list_msg = 'expecting an group list returned by group_list when ' + \
        'called as {0} with data in it, received: {1}'
    group_list_msg = group_list_msg.format(user_label_fixture, group_list)
    assert (group_list != []) == conf_fixture.test_result, group_list_msg
    # now verify that the test group is in the list
    fail_msg = "did not find the test group: {0} in group list: {1} when " + \
        "retrieved as {2}"
    fail_msg = fail_msg.format(test_group, group_list, user_label_fixture)
    assert (test_group in group_list) == conf_fixture.test_result, fail_msg


def test_group_show(conf_fixture, group_create_if_not_exists_fixture,
                           ckan_url, ckan_rest_dir,
                           ckan_auth_header, ckan_apitoken, test_group,
                           user_label_fixture):
    '''
    Verifies the group used for testing can be viewed by all the parameterized
    users
    '''
    LOGGER.debug('test group: %s', test_group)
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'group_show')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_auth_header, params=
                        {'id': test_group})
    group_data = resp.json()
    LOGGER.debug('test group: %s', group_data)

    non_200_msg = 'Returned a status code {0}, expecting 200'.format(
        resp.status_code)
    assert (resp.status_code == 200) == conf_fixture.test_result, non_200_msg

    request_success_msg = 'group_show on {0} returned success {1} as {2}'
    request_success_msg = request_success_msg.format(test_group,
                                                     group_data['success'],
                                                     user_label_fixture)
    assert group_data['success'] == conf_fixture.test_result, request_success_msg
