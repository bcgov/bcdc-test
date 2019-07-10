'''
Created on Jul 8, 2019

@author: kjnether
'''
# pylint: disable=unused-import

import logging

import pytest  # @UnusedImport

import parameterized.helpers.read_test_config

LOGGER = logging.getLogger(__name__)

def pytest_generate_tests(metafunc):

    '''
    Configures parameterization.
        - All tests that should be parameterized should use the:
           - setup_fixtures.data_fixture for data parameterization
           - setup_fixtures.user_label_fixture for user parameterization


    For each test it will:
      - generate a bunch of tests that use different
        user types and
      - different data types


    parameterize:
        - need to be able to return different headers, depending on user
        -

        ckan_auth_header

    https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization-with-multiple-fixtures
    '''
    tst_config_reader = parameterized.helpers.read_test_config.TestConfigReader()
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
