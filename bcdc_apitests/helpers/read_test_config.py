'''
Created on Jul. 3, 2019

@author: kjnether

* store test config in a json file


'''

import pytest
import os.path
import json
import file_utils
import logging


class TestConfigReader(object):
    
    def __init__(self, config_file=None):
        self.logger = logging.getLogger(__name__)
        self.test_config_file = config_file
        if not self.test_config_file:
            fu = file_utils.FileUtils()
            self.test_config_file = fu.get_test_parameter_file_name()
        self.config_struct = self.get_test_config()
    
    def get_test_config(self):
        '''
        reads the test config json file and returns a test config 
        object
        '''
        with open(self.test_config_file, 'r') as myfile:
            test_config_raw = myfile.read()
        config_struct = json.loads(test_config_raw)
        self.logger.debug("config_struct: %s", config_struct)
        return config_struct
        
    def get_test_params(self, module, function):
        '''
        retrieves the test parameters for the given module 
        function
        :param module: the name of the test module that the tests params are for
        :param function: the name of the function that the test params are for.  
        :return: a list of TestParameters objects that apply to the module / function
                 combination.  If no tests are found a blank list is returned
        '''
        test_params = []
        for params in self.config_struct:
            param = TestParameters(params)
            if param.test_module.lower() == module.lower() and \
                    param.test_function.lower() == function.lower():
                test_params.append(param)
        return test_params
        
class TestParameters(object):
    
    def __init__(self, test_param_struct):
        self.logger = logging.getLogger(__name__)
        self.test_param_struct = test_param_struct
        for property in self.test_param_struct:
            self.logger.debug("property: %s", property)
            setattr(self, property, self.test_param_struct[property])
                
# if __name__ == "__main__":
#     LOGGER = logging.getLogger(__name__)
#     LOGGER.setLevel(logging.DEBUG)
#     hndlr = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
#     hndlr.setFormatter(formatter)
#     LOGGER.addHandler(hndlr)
#     LOGGER.debug("test")    
# 
#     
#     
#     test_config = TestConfigReader()
#     testObj = test_config.get_test_config()
#     params = test_config.get_test_params('packages', 'test_add_package_success')
#     
#     print params
        