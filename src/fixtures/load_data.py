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

import ckanapi
import pytest

from .test_config import *


@pytest.fixture
def test_data_dir():
    pkg_json_dir =os.path.join(os.path.dirname(__file__), '..', 'test_data')
    yield pkg_json_dir
    
@pytest.fixture
def test_pkg_data(test_data_dir, test_package):
    logging.debug("test_package: %s", test_package)
    jsonFile = os.path.join(test_data_dir, 'pkgData_min.json')
    with open(jsonFile, 'r') as json_file_hand:
        datastore = json.load(json_file_hand)
        datastore['name'] = test_package
    return datastore

@pytest.fixture
def test_org_data(test_data_dir, test_organization):
    '''
    returns an organization data structure that can be used for testing
    '''
    jsonFile = os.path.join(test_data_dir, 'ownerOrg.json')
    with open(jsonFile, 'r') as json_file_hand:
        org_data = json.load(json_file_hand)
        org_data['name'] = test_organization
    return org_data

@pytest.fixture
def test_group_data():
    pass
