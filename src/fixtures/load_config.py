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
    '''
    :return: full path to the secret file that arms the tests
    '''
    scrt_file = os.path.join(os.path.dirname(__file__), '..', '..', 'secrets', 'secrets.json')
    scrt_file = os.path.realpath(scrt_file)
    logger.debug
    return scrt_file


@pytest.fixture()
def env():
    '''
    :return: the env that the test is set up to run in,
             this value is used by secrets to determine what
             keys to pull from pmp, resources, host names etc
    '''
    return 'TST'


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
    misc_params = creds.getMiscParams()
    token_key = '{0}_TOKEN'.format(env)
    logger.debug("token_key: %s", token_key)
    token = misc_params.getParam(token_key)
    return token

@pytest.fixture()
def ckan_auth_header(ckan_apitoken):
    '''
    authorization header
    '''
    api_headers = {'X-CKAN-API-KEY': ckan_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    return api_headers

@pytest.fixture()
def ckan_restdir(secret_file, ckan_host):
    logger.debug("secretfile: %s", secret_file)
    creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
    misc_params = creds.getMiscParams()
    restdir_key = 'REST_DIR'
    logger.debug("restdir_key: %s", restdir_key)
    restdir = misc_params.getParam(restdir_key)
    return restdir
