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

logger = logging.getLogger(__name__)

#ToDo: get this working at the session level without defining here.
token = os.environ['BCDC_API_KEY']
url = os.environ['BCDC_URL']

# usr_name = 'zztestcriuser1'
# usr_email = 'do_not_reply@gov.bc.ca'
# usr_pass = 'zzztestpassword'


# --------------------- Supporting Functions ----------------------


def check_if_user_exist(remote_api_admin_auth,user):
    usr_exists = False
    try:
        usr_data = remote_api_admin_auth.action.user_show(id=user)
        logger.debug("user found and show: %s", usr_data)
        if usr_data['name'] == user:
            usr_exists = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)

    return usr_exists


def check_if_user_active(remote_api_admin_auth,user):
    usr_active = False
    try:
        usr_data = remote_api_admin_auth.action.user_show(id=user)
        logger.debug("user found and show state: %s", usr_data['state'])
        if usr_data['state'] == "deleted":
            usr_active = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)

    return usr_active


def user_delete(remote_api_admin_auth, user):
    try:
        usr_data = remote_api_admin_auth.action.user_delete(id=user)
        logger.debug("delete user: %s", user)
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)

# --------------------- Fixtures ----------------------

@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown(test_viewer_user, test_admin_user, test_editor_user):
    logger.debug("------------Session-Setup--------------")
    users = (test_viewer_user, test_admin_user, test_editor_user)

    #Todo: find a way to get this to work at the session level without defining here.
    rmt_api = ckanapi.RemoteCKAN(url, token)

    for user in users:
        logger.debug("checking for user account: %s", user)
        exists = check_if_user_exist(rmt_api, user)
        if exists:
            logger.debug("user found")
            active = check_if_user_active(rmt_api, user)

            if active:
                logger.debug("user active")
                try:
                    usr_data = rmt_api.action.user_update(id=user, state='active', email=user)
                    logger.debug("user found and changed state to: %s", usr_data['state'])
                except ckanapi.errors.NotFound as err:
                    logger.debug("err: %s %s", type(err), err)
            else:
                logger.debug("user found and no change to state required")
        else:
            usr_data = rmt_api.action.user_create(name=user, email='test_do_not_reply@gov.bc.ca',
                                                  password='zzztestpassword')
            logger.debug("creating user: %s", str(usr_data))

    yield
    logger.debug("-----------Session Teardown--------------")

    # logger.debug("Cleanup Users: %s", users)
    # for user in users:
    #     user_delete(rmt_api, user)
