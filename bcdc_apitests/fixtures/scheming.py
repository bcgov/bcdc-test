'''
Created on Sep. 26, 2019

@author: KJNETHER

a fixture that can hit the scheming end point returning the json data
schema.
'''

import pytest
import logging
import requests

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def get_scheming(ckan_auth_header, ckan_url, ckan_rest_dir):
    '''
    end point

    https://cadi.data.gov.bc.ca/api/3/action/scheming_dataset_schema_show?type=bcdc_dataset
    '''
    api_call = '{0}{1}/{2}'.format(ckan_url, ckan_rest_dir, 'scheming_dataset_schema_show')
    params = {'type': 'bcdc_dataset'}
    LOGGER.debug(f'api call for scheming: {api_call}')

    resp = requests.get(api_call, params=params)
    resp_data = resp.json()
    resp_result = resp_data['result']
    yield resp_result
