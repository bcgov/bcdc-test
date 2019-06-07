'''
Created on May 13, 2019

@author: KJNETHER

fixtures used for package tests
'''

# from fixtures.load_config import *
# from fixtures.load_data import *
# from fixtures.packages import *
# from fixtures.test_config import *

from ckanext_bcdc_apitests.fixtures.packages import test_pkg_teardown, ckan_rest_dir, test_package_exists  # @UnusedImport
from ckanext_bcdc_apitests.fixtures.ckan import remote_api_admin_auth
from ckanext_bcdc_apitests.fixtures.load_config import ckan_url, ckan_auth_header
from ckanext_bcdc_apitests.fixtures.load_data import test_pkg_data
from ckanext_bcdc_apitests.fixtures.test_config import ckan_rest_dir
