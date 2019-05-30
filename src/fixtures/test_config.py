'''
Created on May 27, 2019

@author: KJNETHER

putting global configuration parameters into this file

'''

import pytest

# Following are test constants
TEST_PREFIX = 'zzztest'
#TEST_ORGANIZATION = '{0}_testorg'.format(TEST_PREFIX)
TEST_ORGANIZATION = 'databcc'
TEST_PACKAGE = '{0}_testpkg'.format(TEST_PREFIX)


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

