'''
Created on May 13, 2019

@author: KJNETHER

trying to set up the fixtures so that they:
- test for 'test' data
- remove 'test' data if it already exists
- re-create test data

'''
import pytest
import os.path
import json
import ckanapi

@pytest.fixture
def test_data_dir():
    pkg_json_dir =os.path.join(os.path.dirname(__file__), '..', 'test_data')
    yield pkg_json_dir
    
@pytest.fixture
def test_pkg_data(test_data_dir):
    jsonFile = os.path.join(test_data_dir, 'pkgData.json')
    with open(jsonFile, 'r') as json_file_hand:
        datastore = json.load(json_file_hand)
    return datastore
