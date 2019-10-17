'''
Created on Sept 13, 2019

@author: KJNETHER

fixtures used to handle command line arguements
'''
import logging
import pytest
from bcdc_apitests.config.testConfig import DF_OPTS

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def df(request, test_disable_teardown_opts):
    '''
    -df: command line switch allows test to run with the option for
         disabling the teardown associated with each test.
    '''
    LOGGER.debug(f'test_disable_teardown_opts: {test_disable_teardown_opts}')
    opt = request.config.getoption("--df")
    LOGGER.debug(f'opt: {opt}, {type(opt)}')
    if opt not in test_disable_teardown_opts and \
        opt is not None:
        msg = f'--df valid options: {test_disable_teardown_opts}. ' + \
             f'Option received: {opt}'
        raise ValueError(msg)
    LOGGER.debug(f"Command line opt: {opt}")
    # now validation
    return opt


@pytest.fixture(scope="session")
def cancel_package_teardown(df):
    cancel_teardown_opts = ['packages', 'ALL', None]
    cancel_teardown = False
    if df in DF_OPTS:
        cancel_teardown = True
    return cancel_teardown


@pytest.fixture(scope="session")
def cancel_org_teardown(df):
    cancel_teardown_opts = ['orgs', 'ALL', None]
    cancel_teardown = False
    if df in DF_OPTS:
        cancel_teardown = True
    return cancel_teardown

@pytest.fixture(scope="session")
def cancel_user_teardown(df):
    cancel_teardown_opts = ['users', 'ALL', None]
    cancel_teardown = False
    if df in DF_OPTS:
        cancel_teardown = True
    return cancel_teardown

@pytest.fixture(scope="session")
def cancel_group_teardown(df):
    cancel_teardown_opts = ['groups', 'ALL', None]
    cancel_teardown = False
    if df in DF_OPTS:
        cancel_teardown = True
    return cancel_teardown

@pytest.fixture(scope="session")
def cancel_resource_teardown(df):
    cancel_teardown_opts = ['resources', 'ALL', None]
    cancel_teardown = False
    if df in DF_OPTS:
        cancel_teardown = True
    return cancel_teardown

@pytest.fixture(scope="session")
def cancel_cache_teardown(df):
    cancel_teardown_opts = ['cache', 'ALL', None]
    cancel_teardown = False
    if df in DF_OPTS:
        cancel_teardown = True
    return cancel_teardown

