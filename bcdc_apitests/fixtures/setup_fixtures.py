'''
Created on Jul 5, 2019

@author: kjnether

These are going to be top level fixtures, ie most fixtures will
cascade/consume these fixtures.

These fixtures are parameterized in the conftest.

The setup for them is described in the test_config

'''
import logging

import pytest

from bcdc_apitests.config.testConfig import BCDC_ROLE_LOOKUP
from bcdc_apitests.config.testConfig import USER_CONFIG

LOGGER = logging.getLogger(__name__)

# pylint: disable=redefined-outer-name

@pytest.fixture
def data_label_fixture(conf_fixture):
    '''
    This fixture will get parameterized by the conftest for the different
    datasets that should be tested.

    Will provide a label/id that is passed down to other fixtures that will
    the decided how the data needs to be configured.

    '''
    # should test to make sure there is only one dataset.
    # assume tests have been flattened if this fixture is called.
    yield conf_fixture.test_data


@pytest.fixture
def user_label_fixture(conf_fixture):
    '''
    parameterized fixture that cycles the different user types to
    be used for the testing, example: viewer, editor, admin

    labels then get consumed by other fixtures to determine what
    they should do.
    '''
    # The conf_fixture refers to the role not the actual user name
    # need to look up the user that has been configured for the
    # specified role and return the user
    user_names = []
    for conf_test_role in conf_fixture.test_users:
        for auth_role_name in BCDC_ROLE_LOOKUP:
            if conf_test_role in BCDC_ROLE_LOOKUP[auth_role_name]:
                conf_test_role = auth_role_name

        # now get the role from the USER_CONFIG
        user_lookup_found = False
        valid_roles = []
        for user in USER_CONFIG:
            valid_roles.append(USER_CONFIG[user]['role'])
            if conf_test_role == USER_CONFIG[user]['role']:
                user_names.append(user)
                user_lookup_found = True
        if not user_lookup_found:
            msg = 'The test configuration references the user: {0} which is ' + \
                  'an invalid value. reference is for the module {1} and ' + \
                  'function: {2}.  Some valid values include: {3}'
            msg = msg.format(conf_test_role, conf_fixture.test_module,
                             conf_fixture.test_function, valid_roles)
            raise UserRoleConfigurationException(msg)
    LOGGER.debug("user_names: %s", user_names)
    yield user_names

@pytest.fixture
def conf_fixture(request):
    '''
    Gets a TestConfig object that contains the test configuration
    information for the module/test combination
    '''
    LOGGER.debug("param for the fixture config: %s", request.param)
    yield request.param


class UserRoleConfigurationException(Exception):
    '''
    exception for when the user / role do not have expected values.
    '''
    pass
