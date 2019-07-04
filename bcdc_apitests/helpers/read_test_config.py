'''
Created on Jul. 3, 2019

@author: kjnether

* store test config in a json file


'''
from functools import partial

import pytest
import os.path
import json

from bcdc_apitests.fixtures.load_data import test_data_dir

def _inject(cls, names):
    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        for name in names:
            setattr(self, name, request.getfixturevalue(name))

    cls.__auto_injector_fixture = auto_injector_fixture
    return cls

def auto_inject_fixtures(*names):
    return partial(_inject, names=names)


@auto_inject_fixtures('test_data_dir')
class TestConfigReader(object):
    
    def __init__(self, config_file=None):
        self.config_file = config_file
        if not self.config_file:
            self.config_file = self.get_config_file_path()
        print 'test_data_dir', self.test_data_dir
    
    def get_config_file_path(self):
        '''
        calculates the config file path using expected 
        relative path
        '''
        # TODO: merge how this path is retrieved with the datadir fixture
    
    def get_test_config(self):
        '''
        reads the test config json file and returns a test config 
        object
        '''
        with open(self.config_file, 'r') as myfile:
            test_config_raw = myfile.read()
        config_struct = json.loads(test_config_raw)
        
        # TODO: create an object that wraps the struct
        
        
        

        
        
if __name__ == "__main__":
    test_config = TestConfigReader()
    
        