'''

Created on May 16, 2019

@author: KJNETHER

Can't test orgs as there is no way to create orgs without superuser


'''
# pylint: disable=invalid-name, unused-argument, too-many-arguments, unused-import
import logging
import requests
import pytest  # @UnusedImport

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name


def test_organization_list(conf_fixture, org_create_if_not_exists_fixture,
                           test_organization, ckan_url, ckan_rest_dir,
                           ckan_auth_header, user_label_fixture):
    '''
    verifies can retrieve a list of organizations and that there is at least
    one org defined
    '''
    # this should be a requests call to verify status
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'organization_list')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_auth_header, params=
                        {'id': test_organization})
    resp_data = resp.json()
    LOGGER.debug("resp json: %s", resp_data)

    # assert that was success and 200
    non_200_msg = 'called the end point organization_list as {0} and returned ' + \
                  'status code: {1}'
    non_200_msg = non_200_msg.format(user_label_fixture, resp.status_code)
    assert resp.status_code == 200, non_200_msg

    success_msg = 'organization_list called as {0} returned success {1}'
    success_msg = success_msg.format(user_label_fixture, conf_fixture.test_result)
    assert resp_data['success'] == conf_fixture.test_result, success_msg

    org_list = resp_data['result']
    LOGGER.debug("orglist: %s", org_list)
    LOGGER.debug("orglist cnt: %s", len(org_list))
    org_list_msg = 'expecting an org list returned by organization_list when ' + \
        'called as {0} with data in it, recieved: {1}'
    org_list_msg = org_list_msg.format(user_label_fixture, org_list)
    assert (org_list != []) == conf_fixture.test_result, org_list_msg
    # now verify that the test org is in the list
    fail_msg = "did not find the test organization: {0} in org list: {1} when " + \
        "retrieved as {2}"
    fail_msg = fail_msg.format(test_organization, org_list, user_label_fixture)
    assert (test_organization in org_list) == conf_fixture.test_result, fail_msg


def test_organization_show(conf_fixture, org_create_if_not_exists_fixture,
                           ckan_url, ckan_rest_dir,
                           ckan_auth_header, ckan_apitoken, test_organization,
                           user_label_fixture):
    '''
    Verifies the org used for testing can be viewed by all the parameterized
    users
    '''
    LOGGER.debug('test org: %s', test_organization)
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'organization_show')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_auth_header, params=
                        {'id': test_organization})
    org_data = resp.json()
    LOGGER.debug('test org: %s', org_data)

    non_200_msg = 'Returned a status code {0}, expecting 200'.format(
        resp.status_code)
    assert (resp.status_code == 200) == conf_fixture.test_result, non_200_msg

    request_success_msg = 'organization_show on {0} returned success {1} as {2}'
    request_success_msg = request_success_msg.format(test_organization,
                                                     org_data['success'],
                                                     user_label_fixture)
    assert org_data['success'] == conf_fixture.test_result, request_success_msg


def test_organization_list_related(conf_fixture, org_create_if_not_exists_fixture,
                           test_organization, ckan_url, ckan_rest_dir,
                           ckan_auth_header, user_label_fixture):
    '''
    verifies can retrieve all organizations and properties and check test org
    exist in results by title
    '''
    # return all fields
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'organization_list_related')
    LOGGER.debug('api_call: %s', api_call)
    resp = requests.get(api_call, headers=ckan_auth_header, params=
                        {'all_fields': True})
    resp_data = resp.json()

    # assert that was success and 200
    non_200_msg = 'called the end point organization_list as {0} and returned ' + \
                  'status code: {1}'
    non_200_msg = non_200_msg.format(user_label_fixture, resp.status_code)
    assert resp.status_code == 200, non_200_msg

    success_msg = 'organization_list called as {0} returned success {1}'
    success_msg = success_msg.format(user_label_fixture, conf_fixture.test_result)
    assert resp_data['success'] == conf_fixture.test_result, success_msg

    org_list = resp_data['result']
    LOGGER.debug("orglist cnt: %s", len(org_list))
    org_list_msg = 'expecting an org list returned by organization_list when ' + \
        'called as {0} with data in it, recieved: {1}'
    org_list_msg = org_list_msg.format(user_label_fixture, org_list)
    assert (org_list != []) == conf_fixture.test_result, org_list_msg
    # now verify that the test org is in the list

    org_found = False

    if not any(org['title'] == test_organization for org in org_list):
        org_found = True
        LOGGER.debug("found {0} in results".format(test_organization))
    fail_msg = "did not find the test organization: {0} in org list: {1} when " + \
        "retrieved as {2}"
    fail_msg = fail_msg.format(test_organization, org_list, user_label_fixture)
    assert org_found == conf_fixture.test_result, fail_msg
