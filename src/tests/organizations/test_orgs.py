'''
Created on May 16, 2019

@author: KJNETHER
'''
import pytest
import ckanapi
import pprint
import logging


logger = logging.getLogger(__name__)

def test_verify_read_orgs(ckan_url):
    '''
    verifies can retrieve orgs..
    '''
    remoteApi = ckanapi.RemoteCKAN(ckan_url)    
    pkgList = remoteApi.action.organization_list()
    logger.debug("orglist cnt: %s", len(pkgList))
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(pkgList)
    assert pkgList
    
def test_add_organization(test_org_data, ckan_url, ckan_apitoken):
    remoteApi = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)
     
    #orgList = remoteApi.action.organization_list_for_user()
    #logger.debug("orgList: %s", orgList)
    pkg_create = remoteApi.action.organization_create(**test_org_data)
    logger.debug("org return data: %s", pkg_create)

