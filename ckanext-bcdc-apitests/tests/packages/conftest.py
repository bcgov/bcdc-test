'''
Created on May 13, 2019

@author: KJNETHER

fixtures used for package tests
'''

# from fixtures.load_config import *
# from fixtures.load_data import *
# from fixtures.packages import *
# from fixtures.test_config import *

from fixtures.ckan import remote_api_admin_auth
from fixtures.load_config import ckan_url, ckan_auth_header
from fixtures.load_data import test_pkg_data
from fixtures.packages import test_pkg_teardown, ckan_rest_dir  # @UnusedImport
from fixtures.test_config import ckan_rest_dir
