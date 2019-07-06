'''
Created on Jul 5, 2019

@author: kjnether
'''
import pytest

import logging

LOGGER = logging.getLogger(__name__)

    

    
@pytest.fixture
def some_other_test_fixture(setup_fixture):
    '''
    This would be dependent fixture, returns logic as oppose to 
    a value
    '''
    LOGGER.debug("user_data_fixture: %s", setup_fixture)
    # now return based on userconfig
    yield setup_fixture

    
    
    

