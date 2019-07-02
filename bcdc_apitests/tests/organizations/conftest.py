'''
Created on May 13, 2019

@author: KJNETHER
'''

import pytest

from bcdc_apitests.fixtures.load_config import *
from bcdc_apitests.fixtures.load_data import *
from bcdc_apitests.fixtures.config_fixture import *
from bcdc_apitests.fixtures.orgs import *
from bcdc_apitests.fixtures.ckan import *



#
# @pytest.fixture(scope="module")
# def org_teardown_fixture(remote_api_admin_auth, test_organization, test_package_exists):
#
#     org_delete(remote_api_admin_auth, test_organization)
#     logger.debug("initial delete of org : %s", test_organization)
#     org_purge(remote_api_admin_auth, test_organization)
#     logger.debug("initial purge of org : %s", test_organization)
#     yield
#     org_delete(remote_api_admin_auth, test_organization)
#     logger.debug("teardown delete of org : %s", test_organization)
#     org_delete(remote_api_admin_auth, test_organization)
#     logger.debug("teardown purge of org : %s", test_organization)
