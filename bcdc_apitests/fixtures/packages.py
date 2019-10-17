'''
Created on May 29, 2019

@author: KJNETHER

Code used to verify packages.
'''
import logging

import ckanapi
import pytest

from .ckan import remote_api_super_admin_auth
from .config_fixture import test_package_name
from bcdc_apitests.fixtures.dynamic_data import populate_bcdc_dataset

import bcdc_apitests.config.testConfig as testConfig

LOGGER = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name, logging-fstring-interpolation
# --------------------- Supporting Functions ----------------------



# need to be able to call directly... don't need to make this a fixture.
def package_delete(remote_api, test_package_name):
    '''
    :param remote_api: a ckanapi remote object
    :param pkg_name: the name of the package that needs to be deleted
    '''
    LOGGER.debug("deleting the package: %s", test_package_name)
    remote_api.action.package_delete(id=test_package_name)


def package_purge(remote_api, pkg_name):
    '''
    :param remote_api: a ckanapi remote object
    :param pkg_name: the name of the package that needs to be deleted
    '''
    LOGGER.debug("purge the package: %s", pkg_name)
    if package_exists(remote_api, pkg_name):
        remote_api.action.dataset_purge(id=pkg_name)


def delete_pkg(remote_api, pkg_name):
    '''
    :param remote_api: a ckan remote api object
    :param pkg_name:  the package name that is to be deleted if it
                      exists.
    '''
    LOGGER.debug("checking for package: %s", pkg_name)
    pkg_exists = package_exists(remote_api, pkg_name)
    if pkg_exists:
        LOGGER.debug("deleting package: %s", pkg_name)
        package_delete(remote_api, pkg_name)
        LOGGER.debug("purge the package: %s", pkg_name)
        remote_api.action.dataset_purge(id=pkg_name)


def set_package_active(remote_api, pkg_name):
    '''
    If the package with the given name exists and it has a state=deleted
    '''
    if package_exists(remote_api, pkg_name, 'ANY'):
        pkg_data = remote_api.action.package_show(id=pkg_name)
        LOGGER.debug("update package...")
        # update for the owner org
        # test org name
        org_data = remote_api.action.organization_show(id=testConfig.TEST_ORGANIZATION)
        org_id = org_data['id']
        LOGGER.debug(f"pkg_data: {pkg_data}")
        if pkg_data['state'] != 'active' or pkg_data['owner_org'] != org_id:
            del pkg_data['resources']
            pkg_data['state'] = 'active'
            pkg_data['owner_org'] = org_id
            LOGGER.debug(f"setting package active and org to: {org_id}")  
            remote_api.action.package_update(**pkg_data)


def package_exists(remote_api, package_name, pkgtype='ANY'):
    '''
    :param remote_api: ckanapi, remote api object that is to be used to determine
                       if the package exists.
    :type remote_api: ckanapi.RemoteCKAN
    :param package_name: the package name or id who's existence is to be
                         determined
    :type package_name: str
    :param pkgtype: the package type that is to be tested for, valid values
        include:
            * ANY - tests for a package whether valid or invalid
            * VALID - tests only for valid packages
            * INVALID - tests only for invalid packages
    '''
    domain = ['ANY', 'VALID', 'INVALID']
    pkgtype = pkgtype.upper()
    if pkgtype not in domain:
        msg = 'specified an illegal pkgtype arguement, valid values include: {0}'
        msg = msg.format(','.join(domain))
        raise ValueError(msg)

    pkg_exists = False
    exists_pkg_type = 'VALID'
    try:
        pkg_data = remote_api.action.package_show(id=package_name)
        LOGGER.debug("package show: %s", pkg_data)
        if pkg_data['name'] == package_name:
            pkg_exists = True
    except ckanapi.errors.NotFound as err:
        LOGGER.debug("err: %s %s", type(err), err)
    except ckanapi.errors.CKANAPIError as err:
        LOGGER.debug("err: %s %s", type(err), err)
        # assume we have a ghost package so yes say exists
        LOGGER.debug("error assuming package exists and is invalid: %s", package_name)
        pkg_exists = True
        exists_pkg_type = 'INVALID'

    # now determine if the package was found whether we are searching for
    # a particular package type, ie valid / invalid
    if pkg_exists and pkgtype != 'ANY':
        # types don't align so the package of the specified type doesn't exist
        if pkgtype != exists_pkg_type:
            pkg_exists = False

    return pkg_exists


# --------------------- Fixtures ----------------------
@pytest.fixture
def package_create_fixture(remote_api_super_admin_auth, populate_bcdc_dataset):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with auth
    :param populate_bcdc_dataset: json that contains a valid object
    '''
    pkg_return = remote_api_super_admin_auth.action.package_create(**populate_bcdc_dataset)
    LOGGER.debug("pkg_return: %s", pkg_return)
    yield pkg_return


@pytest.fixture
def package_create_if_not_exists(remote_api_super_admin_auth,
                                 test_valid_package_exists,
                                 test_invalid_package_exists, data_label_fixture,
                                 populate_bcdc_dataset_single,
                                 org_create_if_not_exists_fixture):
    '''
    :param remote_api_super_admin_auth: ckanapi remote object with super admin
        credentials
    :param test_package_name: the name of the object that should be created
    :param test_valid_package_exists: results of whether the package exists and
        is a valid package
    :param test_valid_package_exists: Does the package exists and is valid, (not
        a ghost package)
    :param populate_bcdc_dataset: the data to use when creating the packages
    '''
    # use the conf_fixture to get the name of the dataset to be used for
    # the test.
    # then call the datapopulator to get the data.
    # data_label_fixture contains the name of the method that's going to return
    # the data.
    LOGGER.debug("calling package_create_if_not_exists")
    pkg_data = None
    data_pkg = populate_bcdc_dataset_single
    LOGGER.debug(f"populate_bcdc_dataset: {data_pkg}")

    test_package_name = data_pkg['name']
    LOGGER.debug("test_package_exists (%s): %s %s", test_package_name,
                 test_package_exists, type(test_package_exists))

    # if a package is found that is invalid it will get deleted and a valid
    # one will be created in its place
    # if test_invalid_package_exists:
    #    LOGGER.debug("invalid package exists, deleting")
    #    package_delete(remote_api_super_admin_auth, test_package_name)
    #    package_purge(remote_api_super_admin_auth, test_package_name)

    if test_valid_package_exists:
        LOGGER.debug("Package exists, loading the data...")
        pkg_data = remote_api_super_admin_auth.action.package_show(
            id=test_package_name)
    else:
        LOGGER.debug("Package does not exist, creating it...")

        pkg_data = remote_api_super_admin_auth.action.package_create(
            **populate_bcdc_dataset_single)
        LOGGER.debug("pkg_return: %s", pkg_data)

    # package should be active and owned by test org
    LOGGER.debug(f"org id: {org_create_if_not_exists_fixture['id']}")
    LOGGER.debug(f"package owner: {pkg_data['owner_org']}")
    if pkg_data['state'] != 'active' or \
        pkg_data['owner_org'] != org_create_if_not_exists_fixture['id']:
        # set package active will also correct the org id
        set_package_active(remote_api_super_admin_auth, data_pkg['name'])

    yield pkg_data


@pytest.fixture
def set_package_state_active(remote_api_super_admin_auth, populate_bcdc_dataset_single):
    LOGGER.debug(f"package name: {populate_bcdc_dataset_single['name']}")
    pckg_shw_data = remote_api_super_admin_auth.action.package_show(id=populate_bcdc_dataset_single['name'])
    if pckg_shw_data['state'] != 'active':
        LOGGER.debug(f"package: {populate_bcdc_dataset_single['name']} state is  {populate_bcdc_dataset_single['state']}")

        pckg_shw_data['state'] = 'active'
        pkg_updt_data = remote_api_super_admin_auth.action.package_update(**pckg_shw_data)
        LOGGER.debug(f'pkg_updt_data: {pkg_updt_data}')


@pytest.fixture
def package_delete_if_exists(remote_api_super_admin_auth, test_package_name,
                             test_package_exists):
    '''
    if the package exists nuke it, differs from test_pkg_teardown that will
    remove the package at teardown stage
    '''
    if test_package_exists:
        package_delete(remote_api_super_admin_auth, test_package_name)


@pytest.fixture
def test_package_exists(remote_api_super_admin_auth, test_package_name):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists
    '''
    LOGGER.debug("testing existence of package: %s", test_package_name)
    exists = package_exists(remote_api_super_admin_auth, test_package_name)
    yield exists


@pytest.fixture
def update_pkg_state(remote_api_super_admin_auth, populate_bcdc_dataset, test_package_state):
    '''
    :param populate_bcdc_dataset: package data structure that can be used to load a new
                          package
    '''
    logging.debug("edc_state Change :: %s", test_package_name)
    populate_bcdc_dataset['edc_state'] = test_package_state
    pkg_data = remote_api_super_admin_auth.action.package_update(**populate_bcdc_dataset)
    LOGGER.debug("pkg_return: %s", pkg_data)
    yield populate_bcdc_dataset


@pytest.fixture
def update_pkg_visibility(remote_api_super_admin_auth, populate_bcdc_dataset, test_package_visibility):
    '''
    :param populate_bcdc_dataset: package data structure that can be used to load a new
                          package
    '''
    logging.debug("metadata_visibility Change :: %s", test_package_name)
    populate_bcdc_dataset['metadata_visibility'] = test_package_visibility
    pkg_data = remote_api_super_admin_auth.action.package_update(**populate_bcdc_dataset)
    LOGGER.debug("pkg_return: %s", pkg_data)
    yield populate_bcdc_dataset


@pytest.fixture
def get_test_package(remote_api_super_admin_auth, test_package_name):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists
    '''
    pkg_data = None
    LOGGER.debug("getting package: %s", test_package_name)
    try:
        pkg_data = remote_api_super_admin_auth.action.package_show(id=test_package_name)
    except ckanapi.errors.CKANAPIError as err:
        LOGGER.debug("err: %s %s", type(err), err)
    yield pkg_data


@pytest.fixture
def package_get_id_fixture(get_test_package):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists
    '''
    pkg_id = None
    if 'id' in get_test_package:
        pkg_id = get_test_package['id']
    yield pkg_id


# trying to remove this, as suspect that that package doesn't show up because it
# is in a deleted state.
@pytest.fixture
def test_invalid_package_exists(remote_api_super_admin_auth, test_package_name):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists

    returns True if the package exists and is valid.
    '''

    LOGGER.debug("testing if a valid package exists: %s", test_package_name)
    exists = package_exists(remote_api_super_admin_auth, test_package_name, 'INVALID')
    yield exists


@pytest.fixture
def test_valid_package_exists(remote_api_super_admin_auth, test_package_name):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with authenticated
    :param test_package_name: the name of a package that exists

    returns True if the package exists and is valid.
    '''
    LOGGER.debug("testing if a valid package exists: %s", test_package_name)
    exists = package_exists(remote_api_super_admin_auth, test_package_name, 'VALID')
    LOGGER.debug(f"valid package exists returns: {exists}")
    yield exists


@pytest.fixture
def test_pkg_teardown(remote_api_super_admin_auth, test_package_name,
                      cancel_package_teardown):
    '''
    :param remote_api_super_admin_auth: a ckanapi remote object with authenticated
    :type param:
    tests to see if the test package exists and removes if it does
    '''
    yield
    if not cancel_package_teardown:
        delete_pkg(remote_api_super_admin_auth, test_package_name)
        package_purge(remote_api_super_admin_auth, test_package_name)
        LOGGER.debug('initial clean up complete')


@pytest.fixture(scope="module")
def module_package_cleaner(remote_api_super_admin_auth, test_package_name,
                           cancel_package_teardown):
    '''
    Run in the conftest, cleans up an test packages before and after the package
    tests are run.
    '''
    if package_exists(remote_api_super_admin_auth, test_package_name):
        delete_pkg(remote_api_super_admin_auth, test_package_name)
    yield
    # teardown
    if not cancel_package_teardown:
        if package_exists(remote_api_super_admin_auth, test_package_name):
            delete_pkg(remote_api_super_admin_auth, test_package_name)

# @pytest.fixture
# def package_recreate(remote_api_super_admin_auth, test_package_name, test_valid_package_exists, test_invalid_package_exists):
#     if test_valid_package_exists or test_invalid_package_exists:
#         delete_pkg(remote_api_super_admin_auth, test_package_name)
#         package_purge(remote_api_super_admin_auth, test_package_name)

