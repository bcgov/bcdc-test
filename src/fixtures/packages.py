'''
Created on May 29, 2019

@author: KJNETHER

Code used to verify packages.
'''
import logging

import ckanapi
import pytest

from fixtures.ckan import *
from fixtures.load_data import *
from fixtures.test_config import *


logger = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name


def package_delete(remote_api, pkg_name):
    '''
    :param remote_api: a ckanapi remote object
    :param pkg_name: the name of the package that needs to be deleted
    '''
    remote_api.action.package_delete(id=pkg_name)


@pytest.fixture
def test_package_exists(remote_api_admin_auth, test_package_name):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists
    '''
    remote_api = remote_api_admin_auth
    pkg_data = None
    pkg_exists = False
    try:
        pkg_data = remote_api.action.package_show(id=test_package_name)
        logger.debug("package show: %s", pkg_data)
        if pkg_data['name'] == test_package_name:
            pkg_exists = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)
    return pkg_exists


@pytest.fixture
def test_pkg_teardown(remote_api_admin_auth, test_package_name, test_package_exists):
    '''
    tests to see if the test package exists and removes if it does
    '''
    if test_package_exists:
        package_delete(remote_api_admin_auth, test_package_name)

