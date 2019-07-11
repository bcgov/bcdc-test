'''
Created on May 28, 2019

@author: KJNETHER
'''
# this set of fixtures is used by other fixtures and all
# tests so need to import globally here.

import logging

import ckanapi
import pytest

from bcdc_apitests.fixtures.config_fixture import *
from bcdc_apitests.fixtures.load_config import *
from bcdc_apitests.fixtures.load_data import *
from bcdc_apitests.fixtures.orgs import *
from bcdc_apitests.fixtures.users import *
from bcdc_apitests.fixtures.ckan import *
from bcdc_apitests.fixtures.setup_fixtures import * 
import helpers.read_test_config

LOGGER = logging.getLogger(__name__)

# ToDo: get this working at the session level without defining here.
# token = os.environ['BCDC_API_KEY']
# url = os.environ['BCDC_URL']


def pytest_generate_tests(metafunc):

    '''
    This is where the automated parameterization takes place.  Code below
    reads the test configuration file (currently: test_data/testParams.json)

    Reads the test_config and parameterizes the fixture
    setup_fixtures/conf_fixture which includes:
      * test data label
      * test user label
      * expectation

    setup is organized so that you can configure each tests parameterization
    in that file, and the code below will implement those definitions.

    https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization-with-multiple-fixtures
    '''
    tst_config_reader = helpers.read_test_config.TestConfigReader()
    test_params = tst_config_reader.get_test_params(module=metafunc.module.__name__,
                                                    function=metafunc.function.__name__)

    LOGGER.debug('module/function: %s/%s', metafunc.module.__name__, metafunc.function.__name__)
    LOGGER.debug('test_params: %s', test_params)
    LOGGER.debug('fixtures required: %s', metafunc.fixturenames)

    if not test_params:
        LOGGER.warning("No parameters are defined for (module/test) %s.%s ",
                       metafunc.module.__name__,
                       metafunc.function.__name__)
    else:
        if 'conf_fixture' in metafunc.fixturenames:
            flat_test_params = test_params.get_flattened()
            test_config_list = flat_test_params.get_test_config_as_list()
            test_config_ids = flat_test_params.get_test_config_ids()
            metafunc.parametrize("conf_fixture",
                                 test_config_list,
                                 ids=test_config_ids,
                                 indirect=True)
    LOGGER.info("completed test parameterization")

# Move this logic into component fixtures that get imported here instead
# of defined here, moved org logic to
# orgs.org_setup_fixture - in theory there is no need to invoke as the
# fixture was tagged autouse.


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown_mod(user_setup_fixture):
    LOGGER.debug("called the session start up")
    pass

# @pytest.fixture(scope="session", autouse=True)
# def session_setup_teardown(test_viewer_user, test_admin_user, test_editor_user,
#                            test_session_organization, session_test_org_data,
#                            session_test_data_dir, remote_api_super_admin_auth):
#     LOGGER.debug("------------Session-Setup--------------")
#
#     # ToDo: find a way to get this to work at the session level without defining here.
#     #rmt_api = ckanapi.RemoteCKAN(url, token)
#     rmt_api = remote_api_super_admin_auth
#     exist = False
#     # setup Org
#     LOGGER.debug("Setup Org: %s", test_session_organization)
#     try:
#         org_data = rmt_api.action.organization_show(id=test_session_organization)
#         LOGGER.debug("org found and show: %s", org_data)
#         exist = True
#     except ckanapi.errors.NotFound as err:
#         LOGGER.debug("err: %s %s", type(err), err)
#         exist = False
#     # create org if not exist
#     if not exist:
#         org_data = rmt_api.action.organization_create(**session_test_org_data)
#
#     # ToDo: cleanup so org_data will exsist if err.
#     org_id = org_data['id']
#     # setup Users
#     users = (test_viewer_user, test_admin_user, test_editor_user)
#     LOGGER.debug("Setup Users: %s", users)
#
#     for user in users:
#         LOGGER.debug("checking for user account: %s", user)
#         exists = check_if_user_exist(rmt_api, user)
#         if exists:
#             LOGGER.debug("user found")
#             active = check_if_user_active(rmt_api, user)
#             if active:
#                 LOGGER.debug("user active")
#                 try:
#                     usr_data = rmt_api.action.user_update(id=user, state='active', email=user)
#                     LOGGER.debug("user found and changed state to: %s", usr_data['state'])
#                 except ckanapi.errors.NotFound as err:
#                     LOGGER.debug("err: %s %s", type(err), err)
#             else:
#                 LOGGER.debug("user found and no change to state required")
#         else:
#             usr_data = rmt_api.action.user_create(name=user, email='test_do_not_reply@gov.bc.ca',
#                                                   password='zzztestpassword')
#             LOGGER.debug("creating user: %s", str(usr_data))
#
#         # find role based on test username
#         if 'admin' in user:
#             role = 'admin'
#             assign_user_role(rmt_api, user, org_id, role)
#         elif 'editor' in user:
#             role = 'editor'
#             assign_user_role(rmt_api, user, org_id, role)
#         elif 'viewer' in user:
#             role = ''
#             # no role for Viewer
#
#     yield
#     LOGGER.debug("-----------Session Teardown--------------")
#
#     LOGGER.debug("Cleanup Users: %s", users)
#     for user in users:
#         user_delete(rmt_api, user)
#
#     LOGGER.debug("Cleanup Org: %s", test_session_organization)
#     org_purge(rmt_api, test_session_organization)
