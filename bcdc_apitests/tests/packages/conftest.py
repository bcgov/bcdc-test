'''
Created on May 13, 2019

@author: KJNETHER

fixtures used for package tests
'''
# pylint: disable=import-error
# pylint: disable=unused-import
from bcdc_apitests.fixtures.packages \
    import \
        test_pkg_teardown, \
        test_package_exists, \
        test_package_name
from bcdc_apitests.fixtures.ckan \
    import \
        remote_api_admin_auth
from bcdc_apitests.fixtures.load_config \
    import \
        ckan_url, \
        ckan_auth_header
from bcdc_apitests.fixtures.load_data \
    import \
        test_pkg_data, \
        test_data_dir, \
        test_pkg_data_core_only, \
        test_org_data
from bcdc_apitests.fixtures.config_fixture \
    import \
        ckan_rest_dir, \
        test_user, \
        test_organization
from bcdc_apitests.fixtures.orgs import *

import pytest
import bcdc_apitests.helpers.read_test_config

def pytest_generate_tests(metafunc):
    '''
    This function should load up the parameters to be 
    used with the package tests.
    
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
    tst_config_reader = bcdc_apitests.helpers.read_test_config.TestConfigReader()
    test_params = tst_config_reader.get_test_params(module=metafunc.module.__name__, 
                                                    function=metafunc.function.__name__)
    # now load up a bunch of tests for the parameters
    # for each parameter configure the user
    # for each parameter configure the dataset
    
    #print 'params', metafunc.function.params
    print 'module name ', metafunc.module.__name__
    print 'function name ', metafunc.function.__name__
    print 'fixtures: ', metafunc.fixturenames
    print '************************************8'
    
    # depending on who the user is send a different api token as "ckan_auth_header"
    # depending on what the dataset is send a different "test_pkg_data"
    funcargs = ['input parameterized data for tests']
    
    #metafunc.addcall(funcargs=funcargs)
    
