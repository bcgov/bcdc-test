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
import bcdc_apitests.helpers.bcdc_dynamic_data_population as bcdc_dynamic_data_population
import bcdc_apitests.config.testConfig as testConfig

LOGGER = logging.getLogger(__name__)

# pylint: disable=logging-fstring-interpolation


@pytest.fixture
def populate_bcdc_dataset(org_create_if_not_exists_fixture, test_package_name,
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

    dataset_populator = bcdc_dynamic_data_population.DataPopulation(ds_schema, 'dataset_fields')
    bcdc_dataset = dataset_populator.populate_randomized(overrides=overrides)

    yield bcdc_dataset

    # teardown code
    if not cancel_cache_teardown:
        LOGGER.debug("calling data cache teardown")
        cache = dataset_populator.cache
        cache.delete_cache()


@pytest.fixture
def populate_bcdc_dataset_single(populate_bcdc_dataset):
    '''
    same thing as populate_bcdc_dataset_single except this method will return a
    single json dataset instead of an iterable containing datasets.
    '''
    LOGGER.debug(f"populate_bcdc_dataset type: {type(populate_bcdc_dataset)}")
    # iterator = iter(populate_bcdc_dataset)
    try:
        dataset = next(populate_bcdc_dataset)
    except StopIteration:
        populate_bcdc_dataset.reset()
        dataset = next(populate_bcdc_dataset)
    LOGGER.debug(f"Dataset Retrieved from iterator: {dataset}")
    yield dataset


@pytest.fixture
def bcdc_dataset_populator(get_scheming):
    '''
    :param get_scheming: the scheming definitions retrieved from the scheming
        end point.

    Test generates a DataPopulation object and returns it.  Individual tests
    will then receive method names through parameterization that belong to the
    object returned by this fixture.  They will call those methods to retrieve
    the data to be used for various tests.
    '''
    dataset_schema = bcdc_dataset_schema.BCDCDataset(
        dataset_type='dataset_fields', struct=get_scheming)

    dataset_populator = bcdc_dynamic_data_population.DataPopulation(
        dataset_schema, 'dataset_fields')
    yield dataset_populator
    
    
@pytest.fixture
def bcdc_resource_populator(get_scheming):
    '''
    :param get_scheming: the scheming definitions retrieved from the scheming
        end point.

    Test generates a DataPopulation object and returns it.  Individual tests
    will then receive method names through parameterization that belong to the
    object returned by this fixture.  They will call those methods to retrieve
    the data to be used for various tests.
    '''
    dataset_schema = bcdc_dataset_schema.BCDCDataset(
        dataset_type='resource_fields', struct=get_scheming)

    dataset_populator = bcdc_dynamic_data_population.DataPopulation(
        dataset_schema, 'resource_fields')
    yield dataset_populator


@pytest.fixture
def populate_resource(get_scheming, package_create_if_not_exists, 
                      bcdc_resource_populator,
                      cancel_cache_teardown):
    '''
    :param get_scheming: the scheming
    gets the scheming defs
    using scheming defs returns a data population object
    '''
    # overrides
    overrides = {"name": testConfig.TEST_RESOURCE,
                 "package_id": package_create_if_not_exists['id'], 
                 "bcdc_type": "geographic"}

    resource_data = bcdc_resource_populator.populate_randomized(overrides)
    LOGGER.debug(f"resource_populator: {bcdc_resource_populator}")
    yield resource_data

    if not cancel_cache_teardown:
        LOGGER.debug("calling data cache teardown")
        cache = bcdc_resource_populator.cache
        cache.delete_cache()


@pytest.fixture
def populate_resource_single(populate_resource, remote_api_super_admin_auth):
    LOGGER.debug(f"resource type: {type(populate_resource)}")
    # iterator = iter(populate_bcdc_dataset)

    #pkg = remote_api_super_admin_auth.action.package_show(id=testConfig.TEST_PACKAGE)

    try:
        resource = next(populate_resource)
    except StopIteration:
        populate_resource.reset()
        resource = next(populate_resource)
    LOGGER.debug(f"Resource Retrieved from iterator: {resource}")
    yield resource
