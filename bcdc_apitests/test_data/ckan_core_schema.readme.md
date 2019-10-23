# ckan_core_schema.json

This file attempts to define the core schema used by ckan in the same way that 
the scheming extension defines our custom schema.  The idea is that for testing 
there is a single way of defining the schema that the dynamic data generator 
will use.

When dynamically generating data to be used in the tests, we can generate either 
ckan_core packages, or the new extended bcdc package type 'bcdc_datset'.  When
generating a bcdc_dataset the types will inherit from the core ckan type.  
Where bcdc_dataset types define the same field as the ckan_core the bcdc_dataset
definition will take precedence.

# Skipped Fields

The following list are fields that make up the CKAN core dataset that are not 
used by bcdc and thus are skipped / not defined in the `ckan_core_schema.json`
file.

  1. package.private
  1. package.tags
  1. package.extras
  1. package.relationships_as_object
  1. package.groups
  1. package.owner_org
  1. resource.size
  1. resource.upload
  1. resource.upload 
