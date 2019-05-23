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

Suggestion for prefix: xxxtest_{object_name}

All data used by the tests will be contained in json files in src/test_data

## Testing

CKAN is made up of the following objects:
 - packages
 - resources
 - organizations
 - groups
 - users
 
Testing will:

Create user, 
Create group
Add user to group
Create organization
Add group to organization
