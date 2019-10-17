'''

Created on Sep 09, 2019

@author: crigdon

'''
# pylint: disable=invalid-name, unused-argument, too-many-arguments, unused-import, logging-format-interpolation
import logging
import requests
import pytest  # @UnusedImport

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name


def test_user_show(conf_fixture, user_label_fixture, remote_api_auth,
                   ckan_url, ckan_auth_header, ckan_rest_dir,
                   test_package_name, package_create_if_not_exists):
    '''
    verify user_show can be retrieved for user that is calling including
    datasets attr and verify pkg is returned in results

    :param param: remote_api_admin_auth

    {"message": "Not found: Group was not found.", '
     '"__type": "Not Found Error"}}')
    '''

    # return all fields
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'user_show')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_auth_header, params=
                        {'id': user_label_fixture, 'include_datasets': True})
    resp_data = resp.json()

    # assert that was success and 200
    non_200_msg = 'called the end point user_show as {0} and returned ' + \
                  'status code: {1}'
    non_200_msg = non_200_msg.format(user_label_fixture, resp.status_code)
    assert resp.status_code == 200, non_200_msg

    success_msg = 'user_show called as {0} returned success {1}'
    success_msg = success_msg.format(user_label_fixture, conf_fixture.test_result)
    assert resp_data['success'] == conf_fixture.test_result, success_msg

# check if user show with datasets includes pkg of test user
    datasets = resp_data['result']['datasets']

    org_found = False

    if not any(pkg['title'] == test_package_name for pkg in datasets):
        org_found = True
        LOGGER.debug("found {0} in results".format(test_package_name))
    fail_msg = "did not find the test pkg: {0} in user show results: {1} when " + \
        "retrieved as {2}"
    fail_msg = fail_msg.format(test_package_name, datasets, user_label_fixture)
    assert org_found == conf_fixture.test_result, fail_msg
