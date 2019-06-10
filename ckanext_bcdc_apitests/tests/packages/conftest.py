'''
Created on May 13, 2019

@author: KJNETHER

fixtures used for package tests
'''
# pylint: disable=import-error
# pylint: disable=unused-import
from ckanext_bcdc_apitests.fixtures.packages \
    import \
        test_pkg_teardown, \
        test_package_exists, \
        test_package_name
from ckanext_bcdc_apitests.fixtures.ckan import remote_api_admin_auth
from ckanext_bcdc_apitests.fixtures.load_config import ckan_url, \
    ckan_auth_header
from ckanext_bcdc_apitests.fixtures.load_data import test_pkg_data, test_data_dir
from ckanext_bcdc_apitests.fixtures.test_config import ckan_rest_dir
