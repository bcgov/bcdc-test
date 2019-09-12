'''
Created on Sept 11, 2019

@author: crigdon

Code used to verify groups.
'''

import logging
import ckanapi
import pytest

LOGGER = logging.getLogger(__name__)
# pylint: disable=redefined-outer-name


@pytest.fixture
def tag_create_fixture(remote_api_super_admin_auth, test_package_name, test_tag, test_tag_data):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    ;param test_package_name: test package name
    :param test_tag_data: the data that is to be used to create the test
        tag
    '''

    LOGGER.debug("tag_return: %s", test_tag_data)
    tag_name = "bob"
    tag_return = remote_api_super_admin_auth.action.package_update(id=test_package_name, tags=[tag_name])
    LOGGER.debug("tag_return: %s", tag_return)


@pytest.fixture
def tag_cleanup_fixture(remote_api_super_admin_auth, test_tag,  test_tag_data):
    '''
    :param remote_api_super_admin_auth: the remote ckanapi object which has
        been authorized with a super admin api token
    :param test_tag_data: the data that is to be used to create the test
        tag
    :param test_tag: the tag name

    '''
    yield
    tag_delete = remote_api_super_admin_auth.action.tag_delete(id=test_tag)
    LOGGER.debug("tag_delete: %s", tag_delete)


