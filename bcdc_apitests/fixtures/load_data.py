'''
Created on May 13, 2019

@author: KJNETHER

trying to set up the fixtures so that they:
- test for 'test' data
- remove 'test' data if it already exists
- re-create test data

'''
import json
import logging
import os.path

import pytest

# pylint: disable=redefined-outer-name

from .config_fixture import test_package_name
from .config_fixture import test_user

from bcdc_apitests.helpers.file_utils import FileUtils
LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def test_data_dir():
    '''
    :return: the data directory
    '''
    file_utils = FileUtils()
    # pkg_json_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    pkg_json_dir = file_utils.get_test_data_dir()
    yield pkg_json_dir


@pytest.fixture
def test_pkg_data(org_create_if_not_exists_fixture, test_data_dir,
                  test_package_name, test_user, data_label_fixture):
    '''
    :param test_data_dir: the data directory fixture, provides the directory
                          where data is located
    :param test_package_name: the name of the test package
    '''
    org_id = org_create_if_not_exists_fixture['id']
    LOGGER.debug("test_package_name: %s", test_package_name)
    LOGGER.debug("test user: %s", test_user)
    json_file = os.path.join(test_data_dir, data_label_fixture[0])
    with open(json_file, 'r') as json_file_hand:
        datastore = json.load(json_file_hand)
        datastore['name'] = test_package_name
        datastore['title'] = '{0} {1}'.format(datastore['title'], test_user)
        datastore['org'] = org_id
        datastore['owner_org'] = org_id
        datastore['sub_org'] = org_id

        # for now removing any group references. Should do group testing later
        # created a ticket to keep track of that issue DDM-738.
        if 'groups' in datastore:
            del datastore['groups']
    return datastore


@pytest.fixture
def resource_data(package_create_if_not_exists, test_data_dir,
                  test_resource_name):
    '''
    :param test_data_dir: The directory where the data files are
        expected to be
    :param test_resource_name: the name of the resource that should
        be used for this test
    '''

    logging.debug("test_resource_name: %s", test_resource_name)
    json_file = os.path.join(test_data_dir, 'resource.json')
    with open(json_file, 'r') as json_file_hand:
        resource = json.load(json_file_hand)
        resource['name'] = test_resource_name
        resource['package_id'] = package_create_if_not_exists['id']
    return resource


@pytest.fixture
def test_pkg_data_core_only(test_pkg_data):
    '''
    :param test_pkg_data: Valid package data

    Method will remove all but the core attributes required as described in
    the ckan docs.

    (https://docs.ckan.org/en/2.8/api/#module-ckan.logic.action.create)

    core attributes:
        - name (string)
        - title (string)
        - private (bool)
        - owner_org (configurable as optional, assuming its not)
    '''
    logging.debug("test_package_name: %s", test_pkg_data)
    core_attribs = ['name', 'title', 'private', 'owner_org']
    core_atribs_only_pkg = {}
    for key in test_pkg_data.keys():
        if key in core_attribs:
            core_atribs_only_pkg[key] = test_pkg_data[key]
    return core_atribs_only_pkg


@pytest.fixture
def test_pkg_data_updated(test_pkg_data):
    '''
    :param test_pkg_data: package data structure that can be used to load a new
                          package
    :return: a ckan package data structure that can be loaded to ckan for testing
    '''
    logging.debug("test_package_name: %s", test_package_name)
    test_pkg_data['title'] = 'test package update'
    return test_pkg_data

@pytest.fixture
def test_pkg_data_prep(test_pkg_data, test_package_state, test_package_visibility):
    '''
    :param test_pkg_data: package data structure that can be used to load a new
                          package
    '''
    logging.debug("test_package_name: %s", test_package_name)
    test_pkg_data['edc_state'] = test_package_state
    test_pkg_data['metadata_visibility'] = test_package_visibility
    return test_pkg_data

@pytest.fixture
def test_org_data(test_data_dir, test_organization):
    '''
    :param test_data_dir: directory where test data is expected
    :param test_organization:  The name to be substituted in for the test organization name
    :return:  an organization data structure that can be used for testing
    '''
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    with open(json_file, 'r') as json_file_hand:
        org_data = json.load(json_file_hand)
        org_data['name'] = test_organization
    return org_data

@pytest.fixture
def test_group_data(test_data_dir, test_group):
    '''
    :param test_data_dir: directory where test data is expected
    :param test_group:  The name to be substituted in for the test organization name
    :return:  an group data structure that can be used for testing
    '''
    json_file = os.path.join(test_data_dir, 'group.json')
    with open(json_file, 'r') as json_file_hand:
        group_data = json.load(json_file_hand)
        group_data['name'] = test_group
    return group_data

@pytest.fixture(scope='session')
def session_test_org_data(test_data_dir, test_session_organization):
    '''
    :return:  an organization data structure that can be used for testing
    '''
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    LOGGER.debug("json file path: %s", json_file)
    with open(json_file, 'r') as json_file_hand:
        org_data = json.load(json_file_hand)
        org_data['name'] = test_session_organization
    return org_data

@pytest.fixture(scope='session')
def session_test_group_data(test_data_dir, test_session_group):
    '''
    :return:  an group data structure that can be used for testing
    '''
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    LOGGER.debug("json file path: %s", json_file)
    with open(json_file, 'r') as json_file_hand:
        group_data = json.load(json_file_hand)
        group_data['name'] = test_session_group
    return group_data