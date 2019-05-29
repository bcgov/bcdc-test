'''
Created on May 14, 2019

@author: KJNETHER

Most of this will get replaced when deployed to pipeline as secrets
could get retrieved from env vars.
'''

import logging
import os.path

import DBCSecrets.GetSecrets
import pytest


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
    '''
    gets the host for the given env
    '''
    # for developing going to use key value pairs, once integrated
    # with jenkins job can configure so that secrets are retrieved from
    # pmp.
    # code below demos how that might work
    #
    # integration with openshift, retrieve these from env vars
    creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
    misc_params = creds.getMiscParams()

    host_key = '{0}_HOST'.format(env)
    logging.debug("host_key: %s", host_key)
    host = misc_params.getParam(host_key)
    return host


@pytest.fixture()
def ckan_url(ckan_host):
    '''
    returns ckan url for the env
    '''
    # for now hard coding the env to DLV, could be TST, PRD
    # env = 'DLV'

    url = 'https://{0}'.format(ckan_host)
    return url


@pytest.fixture()
def ckan_apitoken(secret_file, env):
    '''
    gets the ckan api for the given env
    '''
    creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
    miscParams = creds.getMiscParams()
    token_key = '{0}_TOKEN'.format(env)
    logger.debug("token_key: %s", token_key)
    token = miscParams.getParam(token_key)
    return token

