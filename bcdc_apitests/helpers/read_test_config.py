'''
Created on Jul. 3, 2019

@author: kjnether

* store test config in a json file


'''

import json
import logging

import pytest

import bcdc_apitests.helpers.file_utils


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
            file_util = bcdc_apitests.helpers.file_utils.FileUtils()
            self.test_config_file = file_util.get_test_parameter_file_name()
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
        :return: a TestConfig object that describes all the tests
        :rtype: TestConfig
        '''
        # pylint: disable=no-member
        test_params = []
        for params in self.config_struct:
            param = TestParameters(params)
            if param.test_module.lower() == module.lower() and \
                    param.test_function.lower() == function.lower():
                test_params.append(param)
        test_config = TestConfig(test_params)
        return test_config


class TestConfig(object):
    '''
    This class exists to help make multiple test configurations per
    module/function more easily accessible to the conftest/pytest_generate_tests
    method.

    :ivar testParam: a list composed of TestParameters
    '''

    def __init__(self, test_params):
        self.test_params = test_params
        self.logger = logging.getLogger(__name__)
        self.itercnt = 0
        self.return_list = None
        self.id_list = None

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
            data_list.extend(params.test_data)

        # make unique
        self.logger.debug("data_list: %s", data_list)

        data_set = set(data_list)
        self.logger.debug("data_set: %s", data_set)
        data_list = list(data_list)
        self.logger.debug("unique data_list: %s", data_list)
        self.itercnt = 0
        return data_list

    def get_user_labels(self):
        '''
        :return: iterates over all the test configurations in this object and
        returns a unique list of data labels to be used.
        '''
        user_list = []
        for params in self.test_params:
            user_list.extend(params.test_users)

        user_list = list(set(user_list))
        return user_list

    def __str__(self):
        return str(self.test_params)

    def __next__(self):
        '''
        iteration will iterate over each combination of users and data for the
        current module / function
        '''
        if self.itercnt >= len(self.test_params):
            self.itercnt = 0
            raise StopIteration

        ret_val = self.test_params[self.itercnt]
        self.itercnt += 1
        return ret_val

    def __iter__(self):
        return self

    def get_flattened(self):
        '''
        each test config can have:
          - multiple data sets
          - multiple users
          - a single expected result

        This method will return a new TestConfig object which has been flattened
        so that each TestParameter stored by this object will only have a single
        dataset and a single user.  Flattening will reflect the combinations
        of user / test data.
        '''
        flatter = TestConfig([])
        for params in self:
            for data_label in params.test_data:
                for user_label in params.test_users:
                    self.logger.debug("data_label: %s", data_label)
                    self.logger.debug("user_label: %s", user_label)
                    struct = params.test_param_struct.copy()

                    struct['test_data'] = [data_label]
                    struct['test_users'] = [user_label]
                    self.logger.debug("struct: %s", struct)

                    flat_param = TestParameters(struct)
                    flatter.add_test_params([flat_param])
        return flatter

    def get_test_config_as_list(self, regenerate=True):
        '''
        Works in combination with get_test_config_ids method. this will return a
        list of test configurations, while get_test_config_ids will return a
        list with the test ids.

        The order for both these lists will align.
        '''
        if regenerate:
            self.return_list = None
            self.id_list = None
        if self.return_list is None:
            self.return_list = []
            self.id_list = []
            for params in self:
                self.return_list.append(params)
                test_id = params.get_as_id()
                self.id_list.append(test_id)
        return self.return_list

    def get_test_config_ids(self, regenerate=False):
        '''
        Generates if it doesn't already exist a list of ids for the test
        parameterizations described in this object.
        :param regenerate: if you want to force regeneration of the id list and
                           the test list make this parameter true
        '''
        if regenerate:
            self.id_list = None
        if self.id_list is None:
            self.id_list = []
            self.get_test_config_as_list(regenerate=True)
        return self.id_list


class TestParameters(object):
    '''
    converts a single test paramaterization into an object, allowing for
    retrieval of dictionary keys as properties.

    :ivar test_module: the name of the module that the test is located in.
                       Doesn't require the fully resolved package.module name
                       but rather just the module name.
    :ivar test_function: the name of the function/test in the module that this
                      test config should be applied to.
    :ivar test_user: the user label that the test applied to.  Individual user
                     labels are fetched from the test_data.userConfig.json file.
    :ivar test_data: the data label ( a key word that refers to a test data set
                     configuration) that should be used for this test
                     configuration.
    :ivar test_result: Given all of the above, what is the expected result for
                     the test.
    '''

    def __init__(self, test_param_struct):
        self.test_param_struct = test_param_struct
        for propertee in self.test_param_struct:
            setattr(self, propertee, self.test_param_struct[propertee])

    def __str__(self):
        return str(self.test_param_struct)

    def get_as_id(self):
        '''
        :returns: the autogenerated id for this test parameterization
        '''
        # pylint: disable=no-member
        usr = '/'.join(self.test_users)
        data = '/'.join(self.test_data)

        ret_str = '{0}-{1}-{2}'.format(usr, data, str(self.test_result))
        return ret_str


class TestConfigurationException(Exception):
    '''
    raised when the test configuration file is found to have an incorrect setup
    '''

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
