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
    
    


