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

from .test_config import test_package_name


@pytest.fixture
def test_data_dir():
    '''
    :return: the data directory
    '''
    pkg_json_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
    yield pkg_json_dir


@pytest.fixture
def test_pkg_data(test_data_dir, test_package_name):
    '''
    :param test_data_dir: the data directory fixture, provides the directory
                          where data is located
    :param test_package_name: the name of the test package
    '''
    logging.debug("test_package_name: %s", test_package_name)
    json_file = os.path.join(test_data_dir, 'pkgData_min.json')
    with open(json_file, 'r') as json_file_hand:
        datastore = json.load(json_file_hand)
        datastore['name'] = test_package_name
    return datastore


@pytest.fixture
def test_pkg_data_updated(test_pkg_data):
    '''
    :param test_pkg_data: package data structure that can be used to load a new
                          package
    '''
    logging.debug("test_package_name: %s", test_package_name)
    test_pkg_data['title'] = 'test package update'
    return test_pkg_data


@pytest.fixture
def test_org_data(test_data_dir, test_organization):
    '''
    :return:  an organization data structure that can be used for testing
    '''
    json_file = os.path.join(test_data_dir, 'ownerOrg.json')
    with open(json_file, 'r') as json_file_hand:
        org_data = json.load(json_file_hand)
        org_data['name'] = test_organization
    return org_data
