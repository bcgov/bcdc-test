'''
Created on May 27, 2019

@author: KJNETHER

putting global configuration parameters into this file

'''

import pytest
import getpass
from config.testConfig import *


# pylint: disable=redefined-outer-name


@pytest.fixture(scope='session')
def test_user():
    '''
    :return: the test user letters to be appended to test objects to keep them
        unique between testers
    '''
    return TEST_USER


@pytest.fixture
def test_prefix():
    '''
    :return: the test object naming prefix
    '''
    return TEST_PREFIX


@pytest.fixture(scope='session')
def test_organization():
    '''
    :return: the name of the organization that should be owned by tests
    '''
    return TEST_ORGANIZATION


@pytest.fixture
def test_package_name():
    '''
    :return: the name of the package to be used for the testing.
    '''
    return TEST_PACKAGE


@pytest.fixture
def test_resource_name():
    '''
    :return: the name of the package to be used for the testing.
    '''
    return TEST_RESOURCE


@pytest.fixture
def ckan_rest_dir():
    '''
    :return: the ckan rest dir.
    '''
    return BCDC_REST_DIR

@pytest.fixture(scope="session")
def test_admin_user():
    '''
    :return: the test user letters to be appended to test objects to keep them
        unique between testers
    '''
    return TEST_ADMIN_USER

@pytest.fixture(scope="session")
def test_editor_user():
    '''
    :return: the test user letters to be appended to test objects to keep them
        unique between testers
    '''
    return TEST_EDITOR_USER

@pytest.fixture(scope="session")
def test_viewer_user():
    '''
    :return: the test user letters to be appended to test objects to keep them
        unique between testers
    '''
    return TEST_VIEWER_USER

@pytest.fixture(scope="session")
def test_roles():
    '''
    :return: a list of the different user configs
    '''
    return USER_CONFIG

@pytest.fixture(scope="session")
def test_session_organization():
    '''
    :return: the name of the organization that should be owned by tests
    '''
    return TEST_ORGANIZATION