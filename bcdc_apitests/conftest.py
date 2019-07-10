'''
Created on May 28, 2019

@author: KJNETHER
'''
# this set of fixtures is used by other fixtures and all
# tests so need to import globally here.


import logging
import ckanapi
import pytest

from bcdc_apitests.fixtures.load_config import *
from bcdc_apitests.fixtures.orgs import *
from bcdc_apitests.fixtures.users import *
from bcdc_apitests.fixtures.config_fixture import *
from bcdc_apitests.fixtures.load_data import *
from bcdc_apitests.fixtures.packages import *

logger = logging.getLogger(__name__)

# ToDo: get this working at the session level without defining here.
token = os.environ['BCDC_API_KEY']
url = os.environ['BCDC_URL']
rmt_api = ckanapi.RemoteCKAN(url, token)


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown(test_viewer_user, test_admin_user, test_editor_user, test_session_organization,
                           session_test_org_data, session_test_data_dir, session_test_package_name):

    logger.debug("------------Session-Setup--------------")

    # setup Org
    org_data = org_create_if_not_exists(rmt_api, test_session_organization, session_test_org_data)
    logger.debug("setup org: %s", org_data)
    org_id = org_data['id']

    # setup Users
    users = (test_viewer_user, test_admin_user, test_editor_user)
    logger.debug("setup users: %s", users)

    for user in users:
        logger.debug("checking for user account: %s", user)
        exists = check_if_user_exist(rmt_api, user)
        if exists:
            active = check_if_user_active(rmt_api, user)
            if active:
                update_user(rmt_api, user)
            else:
                logger.debug("user %s is active - no change to state required", user)
        else:
            create_user(rmt_api, user)

        # find role based on test username and set for test org
        if 'admin' in user:
            role = 'admin'
            assign_user_role(rmt_api, user, org_id, role)
        elif 'editor' in user:
            role = 'editor'
            assign_user_role(rmt_api, user, org_id, role)

        # TESTING: get user api key to display
        usr_apikey = get_user_apikey(rmt_api, user)
        logger.debug("user API Key : %s", usr_apikey)

    yield
    logger.debug("-----------Session Teardown--------------")

    logger.debug("Cleanup Users: %s", users)
    for user in users:
        user_delete(rmt_api, user)

    logger.debug("Cleanup Pkg if exists: %s", session_test_package_name)
    package_purge_if_exists(rmt_api, session_test_package_name)

    logger.debug("Cleanup Org if exists: %s", test_session_organization)
    org_purge_if_exists(rmt_api, test_session_organization)
