'''
Created on Jul. 4, 2019

@author: kjnether
'''

import os.path
from bcdc_apitests.config.testConfig import TEST_DATA_DIRECTORY as datadir


class file_utils(object):
    '''
    centralize recovery of file paths
    '''
    def __init__(self):
        pass
    
    def get_data_dir(self):
        '''
        returns the full path to the directory where test data is 
        expected to be located
        :return: test data directory where json test data can be found
        '''
        curdir = os.path.dirname(__file__)
        testFile = os.path.realpath(os.path.join(curdir, '..', datadir, 'testConfig.json'))
        return testFile
