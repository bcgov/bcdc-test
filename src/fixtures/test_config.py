'''
Created on May 27, 2019

@author: KJNETHER

putting global configuration parameters into this file

'''

import pytest

# Following are test constants
TEST_PREFIX = 'zzztest'
#TEST_ORGANIZATION = '{0}_testorg'.format(TEST_PREFIX)
TEST_ORGANIZATION = 'databc'
TEST_PACKAGE = '{0}_testpkg'.format(TEST_PREFIX)

BCDC_REST_DIR = "/api/3/action", 


@pytest.fixture
def test_prefix():
    return TEST_PREFIX

@pytest.fixture
def test_organization():
    # TODO: Change the org to something that currently exists.
    return TEST_ORGANIZATION

@pytest.fixture
def test_package_name():
    return TEST_PACKAGE

@pytest.fixture
def ckan_rest_dir():
    return BCDC_REST_DIR

