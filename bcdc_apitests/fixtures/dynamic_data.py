'''
Created on Oct. 7, 2019

@author: KJNETHER

Fixtures that link to the generation of dynamic data sets.
'''

import json
import logging
import os.path

import pytest

import bcdc_apitests.helpers.bcdc_dataset_schema as bcdc_dataset_schema
import bcdc_apitests.helpers.bcdc_dynamic_data_population as bcdc_dataset_populator

LOGGER = logging.getLogger(__name__)

# pylint: disable=logging-fstring-interpolation


@pytest.fixture
def populate_random(org_create_if_not_exists_fixture, test_package_name,
                    get_scheming, test_package_title,
                    cancel_cache_teardown):
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

    # generate a dataset and then cache it.
    ds_schema = bcdc_dataset_schema.BCDCDataset(dataset_type='dataset_fields',
                           struct=get_scheming)

    # get the scheming data defs
    LOGGER.debug(f'scheming data: {get_scheming}')
    org_id = org_create_if_not_exists_fixture['id']
    overrides = {'owner_org': org_id,
                 'name': test_package_name,
                 'title': test_package_title}

    dataset_populator = bcdc_dataset_populator.DataPopulation(ds_schema)
    bcdc_dataset = dataset_populator.bcdc_dataset_random(overrides=overrides)

    yield bcdc_dataset

    # teardown code
    if not cancel_cache_teardown:
        LOGGER.debug("calling data cache teardown")
        cache = dataset_populator.cache
        cache.delete_cache()


@pytest.fixture
def populate_random_single(populate_random):
    '''
    same thing as populate_random_single except this method will return a
    single json dataset instead of an iterable containing datasets.
    '''
    LOGGER.debug(f"populate_random type: {type(populate_random)}")
    #iterator = iter(populate_random)
    dataset = next(populate_random)
    LOGGER.debug(f"Dataset Retrieved from iterator: {dataset}")
    return dataset


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
