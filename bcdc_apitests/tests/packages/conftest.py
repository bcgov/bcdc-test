'''
Created on May 13, 2019

@author: KJNETHER

fixtures used for package tests
'''
# pylint: disable=import-error
# pylint: disable=unused-import
from bcdc_apitests.fixtures.packages import *
from bcdc_apitests.fixtures.ckan \
    import \
        remote_api_admin_auth
from bcdc_apitests.fixtures.load_config \
    import \
        ckan_url, \
        ckan_auth_header
from bcdc_apitests.fixtures.load_data \
    import \
        test_pkg_data, \
        test_data_dir, \
        test_pkg_data_core_only
from bcdc_apitests.fixtures.config_fixture \
    import \
        ckan_rest_dir, \
        test_user, \
        test_organization
from bcdc_apitests.fixtures.orgs import *
