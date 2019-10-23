'''
Created on Oct. 9, 2019

@author: KJNETHER

When dynamic data is generated it will be caches on the file system.  This module
contains functionality to try to make it easier to deal with cached data

Thinking that caching the data will make it easier to debug when we wind up with
data that do not pass tests.

'''

import logging
import pytest
import os.path

from bcdc_apitests.helpers.file_utils import FileUtils


LOGGER = logging.getLogger(__name__)



@pytest.fixture
def get_cached_package_path(data_label_fixture):
    '''
    :returns: the path to where cached package data is expected to reside
    '''
    # get the directory...
    file_utils = FileUtils()
    cache_dir = file_utils.get_test_data_dir()
    package_path = os.path.join(cache_dir, f'{data_label_fixture}.json')
    LOGGER.debug(f"package path: {package_path}")
    return package_path


    

# gonna delete this fixture and have methods just use the FileUtils class
# @pytest.fixture(scope='session')
# def test_data_dir():
#     '''
#     :return: the data directory
#     '''
#     file_utils = FileUtils()
#     # pkg_json_dir = os.path.join(os.path.dirname(__file__), '..', 'test_data')
#     pkg_json_dir = file_utils.get_test_data_dir()
#     yield pkg_json_dir

