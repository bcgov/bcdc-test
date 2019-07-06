'''
Created on May 15, 2019

@author: KJNETHER

used to verify ability to create packages:

a) create org, retrieve id
    - do round crud test or org.
b) create package with org insert the org just created for this package.

'''

import logging

import ckanapi
import pytest

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

def test_dynamic(user_data_fixture, data_fixture):
    logger.debug("user_data_fixture in test: %s", user_data_fixture)
    logger.debug("data_fixture in test: %s", data_fixture)


def test_something(conf_fixture):
    print 'hello'
    print 'conf_fixture', conf_fixture, type(conf_fixture)
    

