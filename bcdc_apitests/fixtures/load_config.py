'''
Created on May 14, 2019

@author: KJNETHER

Most of this will get replaced when deployed to pipeline as secrets
could get retrieved from env vars.
'''

import logging
import os.path
import pkgutil
import bcdc_apitests.config.testConfig as testConfig

import pytest
import secrets
import string

LOGGER = logging.getLogger(__name__)  # pylint: disable=invalid-name

# declare the namespace to be used by the import if it is optionally imported
DBCSecrets = None  # pylint: disable=invalid-name

# pylint: disable=redefined-outer-name


@pytest.fixture(scope="session")
def import_dbcsecrets():  # @DontTrace
    '''
    Optional import of DBCSecrets, imports if it can be found
    '''
    global DBCSecrets  # pylint: disable=global-statement

    # using the DBC Secrets module if it exists, otherwise will rely on
    # environment variables
    dbc_secrets_exists = pkgutil.find_loader('DBCSecrets')
    LOGGER.debug('dbc_secrets_exists: %s', dbc_secrets_exists)
    if dbc_secrets_exists:
        # can find the package therefor import it
        import DBCSecrets.GetSecrets  # @UnresolvedImport pylint: disable=import-error
        LOGGER.debug('IMPORTED DBCSecrets')
        if 'GetSecrets' in dir(DBCSecrets):
            LOGGER.debug('SUCCESS FOUND DBCSECRETS.GetSecrets')
    yield DBCSecrets


@pytest.fixture(scope="session")
def secret_file():
    '''
    :return: full path to the secret file that arms the tests
    '''
    scrt_file = None
    if testConfig.BCDC_URL not in os.environ:

        scrt_file = os.path.join(os.path.dirname(__file__), '..', '..', 'secrets',
                                 'secrets.json')
        scrt_file = os.path.realpath(scrt_file)
        LOGGER.debug("secret file path: %s", scrt_file)
    LOGGER.debug("yielding: %s", scrt_file)
    yield scrt_file


@pytest.fixture(scope="session")
def env():
    '''
    :return: the env that the test is set up to run in,
             this value is used by secrets to determine what
             keys to pull from pmp, resources, host names etc
    '''
    return 'DLV'


@pytest.fixture(scope="session")
def ckan_host(secret_file, env, import_dbcsecrets):
    '''
    gets the host for the given env
    '''
    # for developing going to use key value pairs, once integrated
    # with jenkins job can configure so that secrets are retrieved from
    # pmp.
    # code below demos how that might work
    #
    # integration with openshift, retrieve these from env vars
    LOGGER.debug('DBCSecrets: %s', DBCSecrets)
    LOGGER.debug('dir: %s', dir())
    LOGGER.debug('dir(DBCSecrets): %s', dir(DBCSecrets))
    LOGGER.debug("Module DBCSecrets can be found: %s",
                 (('DBCSecrets' in dir()) and
                  'GetSecrets' in dir(DBCSecrets)))
    LOGGER.debug('import_dbcsecrets: %s', import_dbcsecrets)
    if testConfig.BCDC_URL in os.environ:
        host = None
        LOGGER.info(f"Env Var BCDC_URL is set: {os.environ[testConfig.BCDC_URL]}",)
    elif 'GetSecrets' in dir(DBCSecrets):
        # if the DBCSecrets module was imported
        LOGGER.debug("using secrets file: %s", secret_file)
        creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
        misc_params = creds.getMiscParams()

        host_key = '{0}_HOST'.format(env)
        logging.debug("host_key: %s", host_key)
        host = misc_params.getParam(host_key)
    else:
        msg = 'unable to retrieve secrets either using the environment ' + \
              f'{testConfig.BCDC_URL} or from the secrets file {secret_file}'
        raise SecretsNotFound(msg)
    yield host


@pytest.fixture(scope="session")
def ckan_url(ckan_host):
    '''
    returns ckan url for the env
    '''
    # for now hard coding the env to DLV, could be TST, PRD
    # env = 'DLV'
    if testConfig.BCDC_URL in os.environ:
        url = os.environ[testConfig.BCDC_URL]
    else:
        url = 'https://{0}'.format(ckan_host)
    yield url


@pytest.fixture(scope="session")
def ckan_superadmin_apitoken(secret_file, env, import_dbcsecrets):
    '''
    Gets the ckan superadmin api token.  Will use this token to generate other
    users.
    '''
    if testConfig.BCDC_API_KEY in os.environ:
        token = os.environ[testConfig.BCDC_API_KEY]
    elif 'GetSecrets' in dir(DBCSecrets):
        LOGGER.debug("GetSecrets module exists, secrets file: %s", secret_file)
        creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
        misc_params = creds.getMiscParams()
        token_key = '{0}_TOKEN'.format(env)
        LOGGER.debug("token_key: %s", token_key)
        token = misc_params.getParam(token_key)
    else:
        LOGGER.debug("secret file: %s", secret_file)
        msg = 'unable to retrieve secrets either using the environment variable ' + \
              f'{testConfig.BCDC_API_KEY} or from the secrets file {secret_file}'
        raise SecretsNotFound(msg)
    yield token


@pytest.fixture(scope="session")
def temp_user_password(import_dbcsecrets, secret_file):
    '''
    The tests generate temp users of various types.  The tests then confirm that
    the security model for these different users types works as expected.  In
    order to generate new users they must be assigned passwords.  This fixture
    generates those passwords.

    How:
      a: looks for the env var BCDC_TMP_USER_PASSWORD if found then just uses
         that as the temporary password
      b: if that doesn't exist then the process will look for secrets.json
         and retrieve from the key for BCDC_TMP_USER_PASSWORD.
      c: if the secret file fails or doesn't exist then the password is
         generated from random numbers.

    If that env var is not found will try to retrieve the password from the
    secrets file.  If it cannot be found there then raises the SecretsNotFound
    error message
    '''
    password = None
    if testConfig.BCDC_TMP_USER_PASSWORD in os.environ:
        password = os.environ[testConfig.BCDC_TMP_USER_PASSWORD]
    elif 'GetSecrets' in dir(DBCSecrets):
        try:
            LOGGER.debug("GetSecrets module exists, secrets file: %s", secret_file)
            creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
            misc_params = creds.getMiscParams()
            passwordkey = 'BCDC_TMP_USER_PASSWORD'
            LOGGER.debug("token_key: %s", '*' * len(passwordkey))
            password = misc_params.getParam(passwordkey)
        except:
            LOGGER.error("unable to get BCDC_TMP_USER_PASSWORD from secret config")
    if password is None:
        # none of the above methods worked to retrieve a password so just
        # going to generate one.
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
    yield password


@pytest.fixture(scope="session")
def ckan_superadmin_auth_header(ckan_superadmin_apitoken):
    '''
    authorization header using the super admin api token.

    super admin is used by fixtures to do setup and tear down.  for the
    most part testing will use a different token.
    '''
    api_headers = {'X-CKAN-API-KEY': ckan_superadmin_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    yield api_headers


@pytest.fixture(scope="session")
def ckan_apitoken_session(user_data_fixture_session):
    '''
    :param user_label_fixture:  identifies the user that should be
                                used for this test
    '''
    # user_label_fixture will be populated with the values in
    # the property test_users from the testParams.json file.
    # they are keywords: admin, editor, viewer
    apitoken = user_data_fixture_session['apikey']
    # for now to make work just continue to use super admin
    # api tokens
    yield apitoken


@pytest.fixture()
def ckan_apitoken(user_data_fixture):
    '''
    :param user_label_fixture:  identifies the user that should be
                                used for this test
    '''
    # user_label_fixture will be populated with the values in
    # the property test_users from the testParams.json file.
    # they are keywords: admin, editor, viewer
    apitoken = user_data_fixture['apikey']
    # for now to make work just continue to use super admin
    # api tokens
    yield apitoken


@pytest.fixture(scope="session")
def ckan_auth_header_session(ckan_apitoken):
    api_headers = {'X-CKAN-API-KEY': ckan_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    yield api_headers


@pytest.fixture()
def ckan_auth_header(ckan_apitoken):
    api_headers = {'X-CKAN-API-KEY': ckan_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    yield api_headers


class SecretsNotFound(Exception):
    """
    Base class for other exceptions
    """

    def __init__(self, message):  # pylint: disable=super-init-not-called
        self.message = message
