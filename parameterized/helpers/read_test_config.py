'''
Created on Jul. 3, 2019

@author: kjnether

* store test config in a json file


'''

import pytest
import os.path
import json
import parameterized.helpers.file_utils
import logging


class TestConfigReader(object):
    '''
    reads the test configuration.  Test configuration comes from a json 
    file that defines:
     - test module name
     - test function name
     - user label to use for test
     - data label to use for test
     - expected result
    '''
    
    def __init__(self, config_file=None):
        self.logger = logging.getLogger(__name__)
        self.test_config_file = config_file
        if not self.test_config_file:
            fu = parameterized.helpers.file_utils.FileUtils()
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
        function.  A single module/function may have multiple records.
        
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
                
        if len(test_params) > 1:
            msg = "The test configuraation file {0}, has more than one configuration " + \
                  "for the test: {1} in the module {2}.  Currently setup can only handle one configuration " + \
                  "per test"
            msg = msg.format(self.test_config_file, function, module)
            raise test_configuration_exception(msg)
        if test_params:
            test_params = test_params[0]
        return test_params
    
class TestConfig(object):
    '''
    This class exists to help make multiple test configurations per 
    module/function more easily accessible to the conftest/pytest_generate_tests
    method.
    
    :ivar testParam: a list composed of TestParameters
    '''
    def __init__(self, test_params):
        self.test_params = test_params
        
    def add_test_params(self, test_params):
        '''
        a new list of test params to be added.
        :param test_params: a list of TestParameters to be added to this object
        '''
        self.test_params.extend(test_params)
        
    def get_data_labels(self):
        '''
        :return: iterates over all the test configurations in this object and
        returns a unique list of data labels to be used.
        '''
        data_list = []
        for params in self.test_params:
            data_list.append(params.test_data)
            
        # make unique
        data_list = list(set(data_list))
        return data_list
    
    def get_user_labels(self):
        '''
        :return: iterates over all the test configurations in this object and
        returns a unique list of data labels to be used.
        '''
        user_list = []
        for params in self.test_params:
            user_list.append(params.test_users)
        
        user_list = list(set(user_list))
        return user_list
    
        
    
    
        
class TestParameters(object):
    '''
    converts a single test paramaterization into an object, allowing for retrieval of 
    dictionary keys as properties.
    
    :ivar test_module: the name of the module that the test is located in.  Doesn't
                       require the fully resolved package.module name but rather just the 
                       module name.
    :ivar test_function: the name of the function/test in the module that this test config
                      should be applied to.
    :ivar test_user: the user label that the test applied to.  Individual user labels are 
                     fetched from the test_data.userConfig.json file.
    :ivar test_data: the data label ( a key word that refers to a test data set configuration)
                     that should be used for this test configuration.
    :ivar test_result: Given all of the above, what is the expected result for the test.    
    '''
    
    def __init__(self, test_param_struct):
        self.logger = logging.getLogger(__name__)
        self.test_param_struct = test_param_struct
        for property in self.test_param_struct:
            self.logger.debug("property: %s", property)
            setattr(self, property, self.test_param_struct[property])
            
    def __str__(self):
        return str(self.test_param_struct)

            
            
class test_configuration_exception(Exception):
    '''
    raised when the test configuration file is found to have an incorrect setup
    '''
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
        
        
                
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
        
