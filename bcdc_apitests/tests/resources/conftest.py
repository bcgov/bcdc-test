'''
Created on Jun. 11, 2019

@author: KJNETHER
'''

from bcdc_apitests.fixtures.packages import *
from bcdc_apitests.fixtures.ckan import *
from bcdc_apitests.fixtures.load_config import *
from bcdc_apitests.fixtures.load_data import *
from bcdc_apitests.fixtures.config_fixture import *
from bcdc_apitests.fixtures.orgs import *


# @pytest.fixture(scope="module")
# def test_pkg_teardown(remote_api_admin_auth, test_package_name, test_package_exists):
#     '''
#     :param remote_api_admin_auth: a ckanapi remote object with authenticated
#     :type param:
#     tests to see if the test package exists and removes if it does
#     '''
#     delete_pkg(remote_api_admin_auth, test_package_name)
#     logger.debug('pre clean up complete')
#     yield
#     delete_pkg(remote_api_admin_auth, test_package_name)
#     logger.debug('post clean up complete')
