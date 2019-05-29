# Overview

A rough plan for how to proceed with the development of api tests.  Overarching
plan for the testing is that all tests will create and cleanup all the data 
needed in order to carry out a sprecific set of tests.

# Plan

## Test Data

Tests will generate their own data required to carry out testing.  This introduces
the possibility of naming conflicts with real/valid data.  Current approach to 
try to avoid this situation will be to append a prefix to all objects created 
by the automated tests.

Suggestion for prefix: zzztest_{object_name}

All data used by the tests will be contained in json files in src/test_data

Object names used for testing should all come from fixtures defined in
`test_config.py`

## Testing

CKAN is made up of the following objects:
 - packages
 - resources
 - organizations
 - groups
 - users
 
 
### Org Testing

**CANNOT CREATE ORGS WITHOUT SUPERADMIN AND THEREFOR CANNOT TEST ORG**
**CREATION UNTIL THAT IS POSSIBLE**

Most objects in CKAN need to belong to an organization.  Only super 
users can create organizations.  The testing will not run under 
super user permissions.  For this reason the testing will start 
with a test_org.  All the data that the tests create will be part 
of this test organization.

The org tests will test much of the code that will be performed by 
fixtures later on in the testing.  

Org testing will:
 * test that sub_org can be created
 * sub org can be updated
 ** add users to sub_org
 ** remove users to sub_org
 * sub org can be deleted


### Package Testing

Package testing takes place after the orgs have been verified.  The 
package testing will:
 
 - create an organiztaion
 - identify data validation problems with org creation... 
    (should not be able to create ghost orgs, that get created
     when a package is created without required fields.  Example 
     is owner_org, when exluded package can be created but ends 
     up being a ghost org.)
 - update package - change resources, etc
 - delete package

### Security Testing

The following is just some ideas, requires further scoping

* Verify read by everyone
* verify idir only datasets
* verify editor permissions
* verify admin permissions.
   * some of these might be taken care of by the creation of orgs
   
Example of the flow for a possible test:

* create an org
* create a package
* Modify security for the package so it should only be viewable
  by idir, verify
* modify security to everyone viewable
  - verify viewable as admin
  - verify viewable as editor
  - verify viewable as reader

