'''
Created on Jul. 4, 2019

@author: kjnether
'''

import os.path
from bcdc_apitests.config.testConfig \
    import \
        TEST_DATA_DIRECTORY as datadir, \
        TEST_PARAMETERS_FILE as tst_params_file


class FileUtils(object):
    '''
    centralize recovery of file paths
    '''

    def __init__(self):
        pass

    def get_test_parameter_file_name(self):
        '''
        returns the full path to the directory where test data is
        expected to be located
        :return: test data directory where json test data can be found
        '''
        datadir_full_path = self.get_test_data_dir()
        test_file = os.path.join(datadir_full_path, tst_params_file)
        return test_file

    def get_test_data_dir(self):
        '''
        :return: the the directory where test data is expected to be located
        '''
        curdir = os.path.dirname(__file__)
        datadir_full_path = os.path.realpath(os.path.join(curdir, '..', datadir))
        return datadir_full_path
