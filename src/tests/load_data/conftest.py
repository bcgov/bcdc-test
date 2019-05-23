'''
Created on May 13, 2019

@author: KJNETHER
'''

import pytest
import logging
import sys

from fixtures.load_config import *
from fixtures.load_data import *

logger = logging.getLogger(__name__)

@pytest.fixture()
def org_list(ckan_url, ckan_apitoken):
    remote_api = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
    org_list = remote_api.action.organization_list()
    return org_list

@pytest.fixture()
def create_org(ckan_url, ckan_apitoken, org_list, test_org_data):
    logger.debug("url: %s", ckan_url)
    remote_api = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
    if test_org_data['name'] not in org_list:
        logger.info("adding the org: %s", test_org_data['name'])
        try:
            #2019-05-16 17:05:05 - 45 - test_package - DEBUG - {u'owner_org': [u'An organization must be provided', u'Missing value'], u'__type': u'Validation Error', u'name': [u'Missing value'], u'title': [u'Missing value']}
            org_data = remote_api.action.organization_create(data_dict=test_org_data)
        except Exception as e:
            logger.debug(e)
            sys.exit()

        
    logger.debug("org_data: %s", org_data)
    return org_data

@pytest.fixture()
def create_get_org(ckan_url, ckan_apitoken, create_org):
    '''
    checks to see if the org defined in ownerOrg 
    exists and if it doesn't creates it.
    
    returns the package id of the package.
    '''
    remote_api = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
    org = remote_api.action.organization_show(name=create_org['name'])
    logger.debug("org is: %s", org)
    return org
