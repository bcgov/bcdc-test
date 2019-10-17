'''
Created on Oct. 15, 2019

@author: KJNETHER

these tests were used to facilitate the development of the helper module
bcdc_dynamic_data_population

'''
# TODO: configure the tests to omit running these tests as they are used for the
#       development of the dynamic datasets
import json
import logging
import os.path
import pprint

import pytest

import bcdc_apitests.helpers.bcdc_dataset_schema as bcdc_dataset_schema
import bcdc_apitests.helpers.bcdc_dynamic_data_population as bcdc_dynamic_data_population

# pylint: disable=logging-fstring-interpolation, redefined-outer-name
# disableing: redefined-outer-name because pylint doesn't properly recognize that
# they are fixtures, and I'm not redefining their scope
LOGGER = logging.getLogger(__name__)
PP = pprint.PrettyPrinter(indent=4)


@pytest.fixture
def scheming_def_from_file():
    '''
    reads the scheming definitions from the cached file.  Using this to speed
    up running of tests when in dev.
    '''
    data_schema_file = os.path.join(os.path.dirname(__file__), '..', 'test_data',
                                    'data_schema.json')
    file_hand = open(data_schema_file, 'r')
    schematext = file_hand.read()
    file_hand.close()
    data_struct = json.loads(schematext)
    yield data_struct


@pytest.fixture
def scheming_bcdc_dataset(scheming_def_from_file):
    '''
    :param scheming_def_from_file: the scheming json data loaded from cache file
    :return: a BCDCDataset scheming object, this is consumed by the populator, this
        is for the datasets
    '''
    # BCDC_Dataset Dataset Fields.
    bcdc_dataset = bcdc_dataset_schema.BCDCDataset(
        dataset_type='dataset_fields', struct=scheming_def_from_file['result'])
    yield bcdc_dataset


@pytest.fixture
def scheming_bcdc_resource(scheming_def_from_file):
    '''
    :param scheming_def_from_file: the scheming json data loaded from cache file
    :return: a BCDCDataset scheming object, this is consumed by the populator, this
        is for the resources
    '''
    # BCDC_Dataset Dataset Fields.
    bcdc_resource = bcdc_dataset_schema.BCDCDataset(
        dataset_type='resource_fields', struct=scheming_def_from_file['result'])
    yield bcdc_resource


def test_summarize_presets(scheming_bcdc_resource, scheming_bcdc_dataset):
    '''
    :param scheming_bcdc_resource: a scheming object populated with resource
        fields
    :type scheming_bcdc_resource: bcdc_apitests.helpers.bcdc_dataset_schema.BCDCDataset
    :param scheming_bcdc_dataset: a scheming object populated with dataset
        fields
    :type scheming_bcdc_resource: bcdc_apitests.helpers.bcdc_dataset_schema.BCDCDataset

    verifies that presets are being populated
    '''
    ds_presets = scheming_bcdc_resource.get_presets()
    resource_preset = scheming_bcdc_dataset.get_presets()

    LOGGER.debug(f"ds_presets: {ds_presets}")
    LOGGER.debug(f"resource_preset: {resource_preset}")

    assert len(ds_presets) > 1
    assert len(resource_preset) > 1

    ds_presets.extend(resource_preset)  # combine presets
    ds_presets = list(set(ds_presets))
    ds_presets.sort()
    LOGGER.debug(f'Unique : {ds_presets}')


def test_dataset_population_random(scheming_bcdc_dataset):
    '''
    :param scheming_bcdc_dataset:  a scheming object populated with dataset rules
    :type scheming_bcdc_dataset:

    used to develop and verify the data returned by populate_randomized
    '''
    dataset_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_dataset, "dataset_fields")
    dataset_populator.disable_cache = True

    bcdc_dataet = dataset_populator.populate_randomized()
    bcdc_dataet.reset()
    ds_iter = iter(bcdc_dataet)
    dataset = next(ds_iter)
    LOGGER.debug(f"Randomized dataset: {dataset}")
    PP.pprint(dataset)


def test_resource_population_random(scheming_bcdc_dataset):
    '''
    :param scheming_bcdc_dataset:  a scheming object populated with dataset rules
    :type scheming_bcdc_dataset:

    used to develop the populate_randomized method
    '''

    resource_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_dataset, "resource_fields")
    resource_populator.disable_cache = True

    resource = resource_populator.populate_randomized()
    resource.reset()
    rs_iter = iter(resource)
    result_set = next(rs_iter)
    LOGGER.debug(f"Randomized dataset: {result_set}")
    PP.pprint(result_set)


def test_rs_population_overrides(scheming_bcdc_resource):
    '''
    :param scheming_bcdc_resource: a scheming object populated with resource
        fields
    :type scheming_bcdc_resource: bcdc_apitests.helpers.bcdc_dataset_schema.BCDCDataset

    '''
    resource_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_resource, "resource_fields")
    resource_populator.disable_cache = True

    # schema... not picking up field_name

    overrides = {'bcdc_type': 'document'}
    ds_iterable = resource_populator.populate_randomized(overrides)
    # all datasets should have the override
    for dataset in ds_iterable:
        for override_field_name in overrides:
            assert override_field_name in dataset
            assert dataset[override_field_name] == overrides[override_field_name]


def test_get_choice_values(scheming_bcdc_resource):
    '''
    :param scheming_bcdc_resource: a scheming object populated with resource
        fields
    :type scheming_bcdc_resource: bcdc_apitests.helpers.bcdc_dataset_schema.BCDCDataset

    shows how to retrieve the choices values for a field def
    '''
    bcdc_type_def = scheming_bcdc_resource.get_field('bcdc_type')

    LOGGER.debug(f"type: {type(bcdc_type_def)}")
    bcdc_choices = bcdc_type_def.choices
    LOGGER.debug(f"bcdc_choices: {bcdc_choices}")
    vals = bcdc_type_def.choices.values
    LOGGER.debug(f'bcdc_type values: {vals}')


def test_get_resource_types(scheming_bcdc_resource):
    '''
    :param scheming_bcdc_resource: a scheming object populated with resource
        fields
    :type scheming_bcdc_resource: bcdc_apitests.helpers.bcdc_dataset_schema.BCDCDataset

    used to develop the populate_bcdc_types method,
    verifies that the datasets returned by the populate_bcdc_types contain all
    the different choices for the field bcdc_type
    '''
    bcdc_type_def = scheming_bcdc_resource.get_field('bcdc_type')
    vals = bcdc_type_def.choices.values

    dataset_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_resource, "resource_fields")
    dataset_populator.disable_cache = True

    bcdc_dataet = dataset_populator.populate_bcdc_types()
    cnt = 0
    for dataset in bcdc_dataet:
        LOGGER.info(f"bcdc_type: {dataset['bcdc_type']}")
        assert dataset['bcdc_type'] in vals
        cnt += 1
    assert cnt == len(vals)
