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
def populate_random(org_create_if_not_exists_fixture, get_scheming):
    '''
       * org_create_if_not_exists_fixture - verifies that the org exists
            and makes org id available
       * test_data_dir - directory where cached version of the file will exist
       * test_package_name - the name the package will recieve
       * test_user - the 3 letter acronym for the test user, used to prevent
           object naming conficts when tests are being run on same instance at
           same time
       * package_cache_file_name - name of the cached version of the dynamically
           generated data.  This file will get created if it doesn't exist at
           startup, and will get deleted at teardown

    * teardown: removes the cached json files created by the dynamic data
    * need to add the switch required to disable teardown
    '''
    # get the scheming data defs
    msg = f'scheming data: {get_scheming}'
    
    # org id, owner_org
    org_id = org_create_if_not_exists_fixture['id']

    bcdc_dataset = bcdc_dataset_schema.BCDCDataset(dataset_type='dataset_fields',
                               struct=get_scheming)
    LOGGER.debug(msg)

    dataset_populator = bcdc_dataset_populator.DataPopulation(bcdc_dataset)
    bcdc_dataet = dataset_populator.populate_random()
    yield bcdc_dataet


@pytest.fixture
def data_population(get_scheming):
    '''
    :param get_scheming: the scheming
    gets the scheming defs
    using scheming defs returns a data population object
    '''
    bcdc_dataset = bcdc_dataset_schema.BCDCDataset(dataset_type='dataset_fields',
                               struct=get_scheming)

    dataset_populator = bcdc_dataset_populator.DataPopulation(bcdc_dataset)
    yield dataset_populator
