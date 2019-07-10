'''
Created on July 08, 2019

@author: crigdon

Code used to boot users.
'''

import logging
import ckanapi
import pytest

logger = logging.getLogger(__name__)

# --------------------- Supporting Functions ----------------------


def check_if_user_exist(remote_api_admin_auth, user):
    usr_exists = False
    try:
        usr_data = remote_api_admin_auth.action.user_show(id=user)
        logger.debug("user found and show: %s", usr_data)
        if usr_data['name'] == user:
            usr_exists = True
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)

    return usr_exists


def check_if_user_active(remote_api_admin_auth, user):
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


def assign_user_role(remote_api_admin_auth, user, org_id, role):
    try:
        resp = remote_api_admin_auth.action.organization_member_create(id=org_id, username=user, role=role)
        logger.debug("setting test user role: %s", resp)
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)


def get_user_apikey(remote_api_admin_auth,user):
    # func must run as sysadmin to return apikey of user
    usr_apiKey = ()
    try:
        usr_data = remote_api_admin_auth.action.user_show(id=user)
        logger.debug("setting test user role: %s", usr_data)
        usr_apiKey = usr_data['apikey']
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)
    return usr_apiKey


def create_user(remote_api_admin_auth,user):
    try:
        usr_data = remote_api_admin_auth.action.user_create(name=user, email='test_do_not_reply@gov.bc.ca',
                                                            password='zzztestpassword')
        logger.debug("Created User: %s", usr_data)
    except ckanapi.errors as err:
        logger.debug("err: %s %s", type(err), err)

def update_user(remote_api_admin_auth,user):
    try:
        usr_data = remote_api_admin_auth.action.user_update(id=user, state='active',
                                                            email='test_do_not_reply@gov.bc.ca')
        logger.debug("user %s found and changed state to: %s", user, usr_data['state'])
    except ckanapi.errors.NotFound as err:
        logger.debug("err: %s %s", type(err), err)