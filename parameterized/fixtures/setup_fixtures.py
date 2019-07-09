'''
Created on Jul 5, 2019

@author: kjnether

These are going to be top level fixtures, ie most fixtures will 
cascade/consume these fixtures.

These fixtures are parameterized in the conftest. 

The setup for them is described in the test_config

'''
import pytest
import logging

LOGGER = logging.getLogger(__name__)

@pytest.fixture
def data_fixture(request):
    '''
    This fixture will get parameterized by the conftest for the different
    datasets that should be tested.
    
    Will provide a label/id that is passed down to other fixtures that will 
    the decided how the data needs to be configured.
    
    '''
    # TODO: Configure so can be run with a single dataset
    yield request.param

@pytest.fixture
def user_label_fixture(request):
    '''
    parameterized fixture that cycles the different user types to 
    be used for the testing, example: viewer, editor, admin
    
    labels then get consumed by other fixtures to determine what
    they should do.
    '''
    # TODO: configure so can be run with a single user label
    yield request.param
    
#TODO: this fixture should be parameterized not user_label_fixture and the 
#      data_fixture.  The conftest pytest_generate_test will read the test
#      configuration and create a conf_test that applies to this specific 
#      test, all the information about the test is injected into this
#      fixture.  If there are a bunch of tests with different users / 
#      datasets they will be described in the config and the conftest will
#      create separate test cases for these.

@pytest.fixture
def conf_fixture(user_label_fixture, data_fixture, expectation):
    '''
    This is always parameterized and recieves:
       dataset_label / user label 
    '''
    yield user_label_fixture, data_fixture
    
@pytest.fixture
def ckan_auth_header2(ckan_apitoken, user_label_fixture):
    '''
    authorization header
    '''
    LOGGER.debug("auth header called from setup, user_label_fixture: %s", user_label_fixture)
    
    api_headers = {'X-CKAN-API-KEY': ckan_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    return api_headers


