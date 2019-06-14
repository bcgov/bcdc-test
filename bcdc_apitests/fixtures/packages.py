'''
Created on May 29, 2019

@author: KJNETHER

Code used to verify packages.
'''
import logging

import ckanapi
import pytest

from .ckan import remote_api_admin_auth
from .test_config import test_package_name

logger = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name

# --------------------- Supporting Functions ----------------------


# need to be able to call directly... don't need to make this a fixture.
def package_delete(remote_api, test_package_name):
    '''
    :param remote_api: a ckanapi remote object
    :param pkg_name: the name of the package that needs to be deleted
    '''
    remote_api.action.package_delete(id=test_package_name)


def delete_pkg(remote_api, pkg_name):
    logger.debug("checking for package: %s", pkg_name)
    pkg_exists = package_exists(remote_api, pkg_name)
    if pkg_exists:
        logger.debug("deleting package: %s", pkg_name)
        package_delete(remote_api, pkg_name)


def package_exists(remote_api, package_name):
    '''
    :param remote_api: ckanapi, remote api object that is to be used to determine
                       if the package exists.
    :type remote_api: ckanapi.RemoteCKAN
    :param package_name: the package name or id who's existence is to be
                         determined
    :type package_name: str
    '''
    pkg_exists = False
    try:
        pkg_data = remote_api.action.package_show(id=package_name)
        logger.debug("package show: %s", pkg_data)
        if pkg_data['name'] == package_name:
            pkg_exists = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)
    except ckanapi.errors.CKANAPIError as err:
        logger.debug("err: %s %s", type(err), err)
        # assume we have a ghost package so yes say exists
        pkg_exists = True
    return pkg_exists


# --------------------- Fixtures ----------------------
@pytest.fixture
def package_create_fixture(remote_api_admin_auth, test_pkg_data):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with auth
    :param test_pkg_data: json that contains a valid object
    '''
    pkg_return = remote_api_admin_auth.action.package_create(**test_pkg_data)
    logger.debug("pkg_return: %s", pkg_return)
    yield pkg_return


@pytest.fixture
def test_package_exists(remote_api_admin_auth, test_package_name):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists
    '''
    logger.debug("testing existence of package: %s", test_package_name)
    exists = package_exists(remote_api_admin_auth, test_package_name)
    yield exists


@pytest.fixture
def test_pkg_teardown(remote_api_admin_auth, test_package_name, test_package_exists):
    '''
    :param remote_api_admin_auth: a ckanapi remote object with authenticated
    :type param:
    tests to see if the test package exists and removes if it does
    '''
    delete_pkg(remote_api_admin_auth, test_package_name)
    logger.debug('initial clean up complete')
    yield
    delete_pkg(remote_api_admin_auth, test_package_name)
    logger.debug('tear down cleanup complete')
