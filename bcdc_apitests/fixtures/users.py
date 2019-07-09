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

