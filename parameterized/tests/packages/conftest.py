'''
Created on May 13, 2019

@author: KJNETHER

fixtures used for package tests
'''
# pylint: disable=import-error
# pylint: disable=unused-import
from parameterized.fixtures.packages import *
from parameterized.fixtures.setup_fixtures import *
from parameterized.fixtures.load_config import *

#from bcdc_apitests.fixtures.load_config import *


import pytest
#import bcdc_apitests.helpers.read_test_config

# def pytest_generate_tests(metafunc):
#     '''
#     This function should load up the parameters to be 
#     used with the package tests.
#     
#     For each test it will:
#       - generate a bunch of tests that use different 
#         user types and 
#       - different data types
#       
#       
#     parameterize:
#         - need to be able to return different headers, depending on user
#         - 
#         
#         ckan_auth_header
#         
#     https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization-with-multiple-fixtures
#     '''
#     #tst_config_reader = bcdc_apitests.helpers.read_test_config.TestConfigReader()
#     #test_params = tst_config_reader.get_test_params(module=metafunc.module.__name__, 
#     #                                                function=metafunc.function.__name__)
#     # now load up a bunch of tests for the parameters
#     # for each parameter configure the user
#     # for each parameter configure the dataset
#     
#     #print 'params', metafunc.function.params
#     print 'module name ', metafunc.module.__name__
#     print 'function name ', metafunc.function.__name__
#     print 'fixtures: ', metafunc.fixturenames
#     print '************************************'
#     
#     
# #     if 'setup_fixture' in metafunc.fixturenames:
# #         metafunc.parametrize("data_fixture",
# #                              ["ds1", "ds2", 'ds3'], 
# #                              ids=['dataset 1', 'dataset 2', 'dataset3'])
# 
#     
#     if 'data_fixture' in metafunc.fixturenames:
#         metafunc.parametrize("data_fixture",
#                              ["ds1", "ds2", 'ds3'], 
#                              ids=['dataset 1', 'dataset 2', 'dataset3'], 
#                              indirect=True)
#     
#     #metafunc.addcall(funcargs=funcargs)
#     if 'user_label_fixture' in metafunc.fixturenames:
#         metafunc.parametrize("user_label_fixture",
#                              ["admin", "editor", 'viewer'], 
#                              ids=['admin user', 'editor user', 'viewer user'],
#                              indirect=True)
#     
    
