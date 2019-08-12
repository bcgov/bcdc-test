'''
Created on Jul 8, 2019

@author: kjnether

Reads the user config file, and acts as an interface to the data stored there.

Currently set up to come from a userConfig.json file in the config
package, but could adapt to come from a better location if identified.

'''

import json
import os.path

import bcdc_apitests.config.testConfig


class user_config(object):
    '''
    a wrapper to the user configuration
    '''

    def __init__(self):
        self.read_user_config()

    def get_user_config_filepath(self):
        '''
        :return:  the user config file path
        '''
        curdir = os.path.dirname(__file__)
        user_config_path = os.path.join(curdir,
                                        '..',
                                        bcdc_apitests.config.testConfig.TEST_DATA_DIRECTORY,
                                        bcdc_apitests.config.testConfig.TEST_USER_CONFIG)
        return os.path.normpath(user_config_path)

    def read_user_config(self):
        '''
        reads the user config file and populates properties of this object
        '''
        config_file = self.get_user_config_filepath()
        with open(config_file) as user_conf:
            self.user_conf_data = json.load(user_conf)

    def get_user_labels(self):
        '''
        :return: the labels used to represent individual users
        '''
        return self.user_conf_data.keys()
