'''
Created on May 28, 2019

@author: KJNETHER
'''
# this set of fixtures is used by other fixtures and all
# tests so need to import globally here.
from bcdc_apitests.fixtures.load_config import *

import pytest
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown(request):
    logger.debug("------------Session Setup--------------")
    yield
    logger.debug("-----------Session Teardown--------------")
