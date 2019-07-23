'''
Created on May 29, 2019

@author: KJNETHER
'''
import pytest
import ckanapi

#from .load_config import ckan_url, ckan_apitoken
from bcdc_apitests.fixtures.load_config import ckan_superadmin_apitoken

# pylint: disable=redefined-outer-name


@pytest.fixture(scope="session")
def remote_api_super_admin_auth(ckan_url, ckan_superadmin_apitoken):
    '''
    :return: a remote ckan object with super admin privs that has been
             authenticated with an api key
    :rtype: ckanapi.RemoteCKAN
    '''
    rmt_api = ckanapi.RemoteCKAN(ckan_url, ckan_superadmin_apitoken)
    yield rmt_api


@pytest.fixture
def remote_api_auth(ckan_url, ckan_apitoken):
    '''
    :return: a remote ckan object with the api token that corresponds with the
             user that was configured by the test parameterization
    :rtype: ckanapi.RemoteCKAN
    '''
    rmt_api = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
    yield rmt_api
