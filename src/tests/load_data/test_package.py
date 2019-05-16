'''
Created on May 15, 2019

@author: KJNETHER

used to verify ability to create packages

'''

import pytest
import ckanapi
import pprint
import logging

logger = logging.getLogger(__name__)

def test_add_package(test_pkg_data, ckan_url, ckan_apitoken):
    '''
    
    '''
    pkgName = test_pkg_data['name']
    logger.debug("apitoken: %s", len(ckan_apitoken))
    remoteApi = ckanapi.RemoteCKAN(ckan_url, ckan_apitoken)   
    pkgList = remoteApi.action.package_list()
    if pkgName in pkgList:
        # remove so can be re-added
        # could also add this to a wrapper fixture that gets called
        # at start and end of everything here.  Leaving it here for
        # now
        logger.debug("cleaning up package: %s", pkgName)
        remoteApi.action.package_delete(pkgName)
    logger.debug("adding the package: %s", pkgName)
    # above line not working but posting anyways as want to share the 
    # skeleton code asap
    pkgSearch = remoteApi.action.package_create(**test_pkg_data)
    
    

    

