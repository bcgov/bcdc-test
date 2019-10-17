'''
Global test properties,

Storing these external to the fixtures so they can be accessed more
easily by helper functions
'''

import getpass

# first three initials of the current test user, using this to keep
# test objects unique allowing multiple dev's to work on test developemnt
# without encountering object naming conflicts

#When run in openshift getuser will fail.  Put the exception in here to use
# ocp as default when this fails.
try:
    TEST_USER = getpass.getuser()[0:3].lower()
except:
    TEST_USER = 'oc'
    
BCDC_TMP_USER_PASSWORD = 'BCDC_TMP_USER_PASSWORD'
    

# all test objects created in ckan should have this prefix appended to them
TEST_PREFIX = "zzztest"

# The directory where the various .json files that contain test data
# are located
TEST_DATA_DIRECTORY = "test_data"
TEST_PARAMETERS_FILE = 'testParams.json'
TEST_USER_CONFIG = "userConfig.json"
TEST_CKAN_CORE_SCHEMA_DEF = 'ckan_core_schema.json'

# test org name
TEST_ORGANIZATION = '{0}_{1}_testorg'.format(TEST_PREFIX, TEST_USER)

# test group name
TEST_GROUP = '{0}_{1}_testgroup'.format(TEST_PREFIX, TEST_USER)

# test package name
TEST_PACKAGE = '{0}_{1}_testpkg'.format(TEST_PREFIX, TEST_USER)

# test package title
TEST_PACKAGE_TITLE = '{0} {1} testpkg title'.format(TEST_PREFIX, TEST_USER)

# test resource name
TEST_RESOURCE = '{0}_{1}_testresource'.format(TEST_PREFIX, TEST_USER)

# path to the rest api
BCDC_REST_DIR = "/api/3/action"

# allows multple names to refer to a single role
BCDC_ROLE_LOOKUP = {'member': ['view', 'viewer', 'looker']}

# user configuration, contains all the informaiton necessary to create these
# new users.
TEST_ADMIN_USER = '{0}_{1}_admin'.format(TEST_PREFIX, TEST_USER)
TEST_EDITOR_USER = '{0}_{1}_editor'.format(TEST_PREFIX, TEST_USER)
TEST_VIEWER_USER = '{0}_{1}_viewer'.format(TEST_PREFIX, TEST_USER)

# default test passwords will need to be retrieved as a secret
USER_CONFIG = {TEST_EDITOR_USER:
               {'email': 'test_editor@gov.bc.ca',
                'role': 'editor'},
               TEST_VIEWER_USER:
               {'email': 'test_viewer@gov.bc.ca',
                'role': 'member'},
               TEST_ADMIN_USER:
               {'email': 'test_admin@gov.bc.ca',
                'role': 'admin'},
               }

# package state and visibility
TEST_STATE = 'draft' # draft,published,pending published
TEST_VISIBILITY = 'IDIR'  # PUBLIC, IDIR

TEST_PACKAGE_STATE = TEST_STATE
TEST_PACKAGE_VISIBILITY = TEST_VISIBILITY

# these are the options that can be sent to the --df flag. The --df flag
# allows you to disable the teardown associated with certain object types
DF_OPTS = ['orgs', 'groups', 'packages', 'resources', 'users', 'other', 'cache', 'ALL', 'none']

# The name of the environment variable that the tests are expecting to retrieve
# api keys from
BCDC_API_KEY = 'BCDC_API_KEY'
BCDC_URL = 'BCDC_URL'
