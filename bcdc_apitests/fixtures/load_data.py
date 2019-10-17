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

# @pytest.fixture
# def populate_bcdc_dataset(org_create_if_not_exists_fixture, get_cached_package_path,
#                   test_package_name, test_user):
#     '''
#     :param org_create_if_not_exists_fixture: creates the test org if it doesn't
#         already exist.
#     :param test_data_dir: the data directory fixture, provides the directory
#         where data is located
#     :param test_package_name: the name of the test package
#
#     assumption is that the 'data_label_fixture' is the name of a method in
#     .helpers.bcdc_dynamic_data_population.DataPopulation. That method
#     is going to get called and the returning data is what will get returned
#
#     #TODO: 9-26-2019 in the middle of implementing what is described above.
#
#     '''
#
#
#
#
#     org_id = org_create_if_not_exists_fixture['id']
#     LOGGER.debug("test_package_name: %s", test_package_name)
#     LOGGER.debug("test user: %s", test_user)
#     json_file = os.path.join(test_data_dir, data_label_fixture[0])
#     with open(json_file, 'r') as json_file_hand:
#         datastore = json.load(json_file_hand)
#         datastore['name'] = test_package_name
#         datastore['title'] = '{0} {1}'.format(datastore['title'], test_user)
#         datastore['org'] = org_id
#         datastore['owner_org'] = org_id
#         datastore['sub_org'] = org_id
#
#         # for now removing any group references. Should do group testing later
#         # created a ticket to keep track of that issue DDM-738.
#         if 'groups' in datastore:
#             del datastore['groups']
#     return datastore


@pytest.fixture
def resource_data(package_create_if_not_exists,
                  test_resource_name):
    '''
    :param test_data_dir: The directory where the data files are
        expected to be
    :param test_resource_name: the name of the resource that should
        be used for this test
    '''
    test_data_dir = FileUtils().get_test_data_dir()
    logging.debug("test_resource_name: %s", test_resource_name)
    json_file = os.path.join(test_data_dir, 'resource.json')
    with open(json_file, 'r') as json_file_hand:
        resource = json.load(json_file_hand)
        resource['name'] = test_resource_name
        resource['package_id'] = package_create_if_not_exists['id']
    return resource


@pytest.fixture
def test_pkg_data_core_only(populate_bcdc_dataset):
    '''
    :param populate_bcdc_dataset: Valid package data

    Method will remove all but the core attributes required as described in
    the ckan docs.

    (https://docs.ckan.org/en/2.8/api/#module-ckan.logic.action.create)

    core attributes:
        - name (string)
        - title (string)
        - private (bool)
        - owner_org (configurable as optional, assuming its not)
    '''
    logging.debug("test_package_name: %s", populate_bcdc_dataset)
    core_attribs = ['name', 'title', 'private', 'owner_org']
    core_atribs_only_pkg = {}
    for key in populate_bcdc_dataset.keys():
        if key in core_attribs:
            core_atribs_only_pkg[key] = populate_bcdc_dataset[key]
    return core_atribs_only_pkg


@pytest.fixture
def test_pkg_data_updated(populate_bcdc_dataset):
    '''
    :param populate_bcdc_dataset: package data structure that can be used to load a new
                          package
    :return: a ckan package data structure that can be loaded to ckan for testing
    '''
    logging.debug("test_package_name: %s", test_package_name)
    populate_bcdc_dataset['title'] = 'test package update'
    return populate_bcdc_dataset


@pytest.fixture
def test_pkg_data_prep(populate_bcdc_dataset, test_package_state, test_package_visibility):
    '''
    :param populate_bcdc_dataset: package data structure that can be used to load a new
                          package
    '''
    logging.debug("test_package_name: %s", test_package_name)
    populate_bcdc_dataset['edc_state'] = test_package_state
    populate_bcdc_dataset['metadata_visibility'] = test_package_visibility
    return populate_bcdc_dataset


@pytest.fixture
def test_org_data(test_organization):
    '''
    :param test_data_dir: directory where test data is expected
    :param test_organization:  The name to be substituted in for the test organization name
    :return:  an organization data structure that can be used for testing
    '''
    test_data_dir = FileUtils().get_test_data_dir()
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    with open(json_file, 'r') as json_file_hand:
        org_data = json.load(json_file_hand)
        org_data['name'] = test_organization
    return org_data


@pytest.fixture
def test_group_data(test_group):
    '''
    :param test_data_dir: directory where test data is expected
    :param test_group:  The name to be substituted in for the test organization name
    :return:  an group data structure that can be used for testing
    '''
    test_data_dir = FileUtils().get_test_data_dir()
    json_file = os.path.join(test_data_dir, 'group.json')
    with open(json_file, 'r') as json_file_hand:
        group_data = json.load(json_file_hand)
        group_data['name'] = test_group
    return group_data

@pytest.fixture(scope='session')
def session_test_org_data(test_session_organization):
    '''
    :return:  an organization data structure that can be used for testing
    '''

    test_data_dir = FileUtils().get_test_data_dir()
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    LOGGER.debug("json file path: %s", json_file)
    with open(json_file, 'r') as json_file_hand:
        org_data = json.load(json_file_hand)
        org_data['name'] = test_session_organization
    return org_data


@pytest.fixture(scope='session')
def session_test_group_data(test_session_group):
    '''
    :return:  an group data structure that can be used for testing
    '''
    test_data_dir = FileUtils().get_test_data_dir()
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    LOGGER.debug("json file path: %s", json_file)
    with open(json_file, 'r') as json_file_hand:
        group_data = json.load(json_file_hand)
        group_data['name'] = test_session_group
    return group_data
