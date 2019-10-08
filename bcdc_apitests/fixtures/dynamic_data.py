'''
Created on Oct. 7, 2019

@author: KJNETHER

Fixtures that link to the generation of dynamic data sets.
'''

import pytest
import logging
import bcdc_apitests.helpers.bcdc_dynamic_data_population as bcdc_dataset_populator
import bcdc_apitests.helpers.bcdc_dataset_schema as bcdc_dataset_schema

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def populate_random(get_scheming):
    '''
    generates random data based on the contents of the scheming ckan extension, 
    
    returns a single dataset with a 
    '''
    # get the scheming data defs
    msg = f'scheming data: {get_scheming}'
    
    bcdc_dataset = bcdc_dataset_schema.BCDCDataset(dataset_type='dataset_fields',
                               struct=get_scheming)
    LOGGER.debug(msg)
    
    dataset_populator = bcdc_dataset_populator.DataPopulation(bcdc_dataset)
    bcdc_dataet = dataset_populator.populate_random()
    yield bcdc_dataet
