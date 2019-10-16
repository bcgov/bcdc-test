'''
Created on Oct. 15, 2019

@author: KJNETHER

Tests to verify the functionality of the helper module bcdc_dynamic_data_population

'''
# TODO: configure the tests to omit running these tests as they are used for the
#       development of the dynamic datasets
import os.path
import json
import logging
import bcdc_apitests.helpers.bcdc_dataset_schema as bcdc_dataset_schema
import bcdc_apitests.helpers.bcdc_dynamic_data_population as bcdc_dynamic_data_population
import pytest
import pprint

LOGGER = logging.getLogger(__name__)
PP = pprint.PrettyPrinter(indent=4)


@pytest.fixture
def scheming_def_from_file():
    dataSchemaFile = os.path.join(os.path.dirname(__file__), '..', 'test_data',
                                  'data_schema.json')
    fh = open(dataSchemaFile, 'r')
    schematext = fh.read()
    fh.close()
    data_struct = json.loads(schematext)
    yield data_struct


@pytest.fixture
def scheming_bcdc_dataset(scheming_def_from_file):
    # BCDC_Dataset Dataset Fields.
    bcdc_dataset = bcdc_dataset_schema.BCDCDataset(
        dataset_type='dataset_fields', struct=scheming_def_from_file['result'])
    yield bcdc_dataset


@pytest.fixture
def scheming_bcdc_resource(scheming_def_from_file):
    # BCDC_Dataset Dataset Fields.
    bcdc_resource = bcdc_dataset_schema.BCDCDataset(
        dataset_type='resource_fields', struct=scheming_def_from_file['result'])
    yield bcdc_resource


def test_summarize_presets(scheming_bcdc_resource, scheming_bcdc_dataset):
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
    dataset_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_dataset, "dataset_fields")
    dataset_populator.disable_cache = True

    bcdc_dataet = dataset_populator.populate_randomized()
    bcdc_dataet.reset()
    ds_iter = iter(bcdc_dataet)
    ds = next(ds_iter)
    LOGGER.debug(f"Randomized dataset: {ds}")
    PP.pprint(ds)


def test_resource_population_random(scheming_bcdc_dataset):
    
    resource_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_dataset, "resource_fields")
    resource_populator.disable_cache = True

    resource = resource_populator.populate_randomized()
    resource.reset()
    rs_iter = iter(resource)
    rs = next(rs_iter)
    LOGGER.debug(f"Randomized dataset: {rs}")
    PP.pprint(rs)


def test_rs_population_overrides(scheming_bcdc_resource):
    resource_populator = bcdc_dynamic_data_population.DataPopulation(
        scheming_bcdc_resource, "resource_fields")
    resource_populator.disable_cache = True

    # schema... not picking up field_name

    overrides = {'bcdc_type': 'document'}
    ds_iterable = resource_populator.populate_randomized(overrides)
    # all datasets should have the override
    for ds in ds_iterable:
        for override_field_name in overrides:
            assert override_field_name in ds
            assert ds[override_field_name] == overrides[override_field_name]

def test_get_choice_values(scheming_bcdc_resource):
    bcdc_type_def = scheming_bcdc_resource.get_field('bcdc_type')
    
    LOGGER.debug(f"type: {type(bcdc_type_def)}")
    bcdc_choices = bcdc_type_def.choices
    LOGGER.debug(f"bcdc_choices: {bcdc_choices}")
    vals = bcdc_type_def.choices.values
    LOGGER.debug(f'bcdc_type values: {vals}')
    

