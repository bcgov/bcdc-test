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
from bcdc_apitests.fixtures.users import *
from bcdc_apitests.fixtures.orgs import *
from bcdc_apitests.fixtures.groups import *
from bcdc_apitests.fixtures.ckan import *
from bcdc_apitests.fixtures.setup_fixtures import *
from bcdc_apitests.fixtures.arguements import *
from bcdc_apitests.fixtures.dynamic_data import *
from bcdc_apitests.fixtures.scheming import *
import bcdc_apitests.helpers.read_test_config as helper
import bcdc_apitests.config.testConfig as DF_OPTS
import bcdc_apitests.helpers.bcdc_dynamic_data_population

LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    LOGGER.debug(f"df opts are: {DF_OPTS}")
    helpstr = f'Optional disabling of teardown code, options include: {DF_OPTS}'
    parser.addoption(
        "--df", action="store", default=None, help=helpstr
    )


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
    tst_config_reader = helper.TestConfigReader()
    test_params = tst_config_reader.get_test_params(module=metafunc.module.__name__,
                                                    function=metafunc.function.__name__)

    # TODO: need to print test_params to make sure they are correct

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


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown_mod(user_setup_fixture):
    '''
    user_setup_fixture - creates the test users, this fixture has a dependency
    to orgs, which will create the test org.

    The session fixtures that create the users and the orgs also have teardown
    code to remove them when the tests are complete

    This fixture only ensures that these fixtures get triggered.
    '''
    LOGGER.debug("called the session start up")

    # at startup and tear down make sure the cache dir is empty
    cache = bcdc_apitests.helpers.bcdc_dynamic_data_population.DataCache('dummy')
    cache.delete_all_caches()
    yield
    cache.delete_all_caches()
