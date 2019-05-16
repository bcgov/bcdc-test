'''
Created on May 14, 2019

@author: KJNETHER

Most of this will get replaced when deployed to pipeline as secrets
could get retrieved from env vars.
'''

import pytest
import DBCSecrets.GetSecrets
import logging
import os.path

logger = logging.getLogger(__name__)

@pytest.fixture()
def secret_file():
    
    scrt_file = os.path.join(os.path.dirname(__file__), '..', '..', 'secrets', 'secrets.json')
    scrt_file = os.path.realpath(scrt_file)
    return scrt_file

@pytest.fixture()
def env():
    return 'DLV'
    
@pytest.fixture()
def ckan_host(secret_file, env):
    # for developing going to use key value pairs, once integrated 
    # with jenkins job can configure so that secrets are retrieved from 
    # pmp.
    # code below demos how that might work
    # 
    # integration with openshift, retrieve these from env vars
    creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
    miscParams = creds.getMiscParams()

    hostKey = '{0}_HOST'.format(env)
    logging.debug("hostKey: %s", hostKey)
    print 'hostKey', hostKey
    host = miscParams.getParam(hostKey)
    return host

@pytest.fixture()
def ckan_url(ckan_host):
    '''
    
    '''
    # for now hard coding the env to DLV, could be TST, PRD
    #env = 'DLV'
    
    url = 'https://{0}'.format(ckan_host)
    return url

@pytest.fixture()
def ckan_apitoken(secret_file, env):
    creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
    miscParams = creds.getMiscParams()
    token_key = '{0}_TOKEN'.format(env)
    logger.debug("token_key: %s", token_key)
    token = miscParams.getParam(token_key)
    return token
    
    
    