'''
Created on May 13, 2019

@author: KJNETHER

Methods relating the verify package data returned by api.

'''
import pytest
import ckanapi
import pprint

def test_verify_package_count(ckan_url):
    '''
    verify the count reported by package_search matches packages
    returned by package_list
    '''
    # verify that the pkg_search and package_list report the same
    # total number of packages
    remoteApi = ckanapi.RemoteCKAN(ckan_url)    
    pkgList = remoteApi.action.package_list()
    pkgSearch = remoteApi.action.package_search()
    assert pkgSearch['count'] == len(pkgList)
    
    
   
    
    
    