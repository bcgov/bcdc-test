# Parameterization

## Overview / How it works

Most if not all of the tests that need to be built to test the BCDC API require
the ability to query one end point using different:
  - Users
  - Data
  
For example the end point (package_create)[https://docs.ckan.org/en/2.8/api/#ckan.logic.action.create.package_create]
For that end point we will want to verify that editors and administrators can
create packages, however viewers should not.  What we are trying to avoid is 
having to write a different test for ever combination of data and user.  The 
solution is to be able to create parameterized tests that re-use the same 
end point with different users, data, and expected results.

The pattern that is to be used to accomplish this for the BCDC api will use the
pytest hook *pytest_generate_tests*.  The hook is implemented in the tests root 
conftest.py. 

When tests are run the hook is called which will read the 
[test configuration file](#test-configuration-file) and create however number
of parameterized tests are required based on the combinations of test data and 
users.   
   
## Test Configuration File

All BCDC api tests that are to be parameterized need to be described in the
file `bcdc_apitests/test_data/testParams.json`. Each record in the file 
describes:

* the module a test exists within
* the name of the test 
* the data to be used in the test
* the users that should be used in the test
* the expected outcome.

Each record in the test config can only have *ONE* outcome.  If you expect different
outcomes depending on the data / user combinations, you need to break of those
combinations into groups of the same outcome.  Take package_create for example.
With the test for this end point we want to:
- verify that admin / editor can successfully create records with two different 
  datasets/packages.
- verify that viewer can *NOT* create packages regardless of what data is used.
- verify that the admin / editor attempts to create records with invalid data
  are no
    
Each of those bullet point describes a different combination of users / data / 
outcome and therefore are described in the Test Configuration File as separate 
records.

### Fields in the Configuration File

* **test_module**   : the name of the module where the test will be found
* **test_function** : the name of the test function to be parameterized
* **test_users**    : a list of test users to be used in this test
* **test_data**     : a list of the datasets to be used this test. These files are expected to be located in the test_data folder.
* **test_result**   : the expected outcome for the all combinations of users and data.

## Fixtures Impacted by Parameterization

### setup_fixtures.conf_fixture

This fixture is the root  of all parameterization.  All other fixtures that use
parameterization do so by declaring this fixture as a requirement.  Other fixtures
or tests that require parameterized values will retrieve them from this fixture.

This fixture will return a `helpers.read_test_config.TestParameters` object.

The properties of this object will be the same as the properties described in the 
test configuration file.  I.e.:

* **test_module** 
* **test_function**
* **test_users**
* **test_data**
* **test_result**

# Creating a Parameterized Test

## Include the setup_fixtures.conf_fixture

If your test is going to be parameterized, make sure it requires the conf_fixture 
fixture.  This fixture will include all the parameterization info required for
your test.  In most cases the only property that you will have to retrieve is 
the `conf_fixture.test_result` property to get the expected results. For 
example:

```python
def some_great_test(conf_fixture, other_fixtures)"
    var = 'some var'
    ... blah blah blah
    
    assert (var == 'expected_var') == conf_fixture.test_result
```

## Existing Fixtures Affected by Parameterization

### Dependency Chains

The following tries to document top level fixtures impacted by parameterization
and then below that identify the dependency chain that takes you back to the 
`setup_fixtures.conf_fixtures`

#### ckan.remote_api_auth

Returns a [ckanapi.RemoteCKAN](https://github.com/ckan/ckanapi#remoteckan) object
that has been created with the api key that corresponds with the parameterized
user.  If your test interacts with CKAN using the ckanapi, this is the fixture 
to use.

```
ckan.remote_api_auth
    <-- load_config.ckan_apitoken
        <--- users.user_data_fixture
            <-- setup_fixtures.user_label_fixture
                <-- setup_fixtures.conf_fixture
```

#### load_config.ckan_auth_header

If your test is a lower level test that constructs the rest call using requests
or some other library, then this is likely the fixture you will want to to use.
It will feed your test with the api_token for the various users that your test
will be run with.

```
load_config.ckan_auth_header
    <-- load_config.ckan_apitoken
        <--- users.user_data_fixture
            <-- setup_fixtures.user_label_fixture
                <-- setup_fixtures.conf_fixture

```


