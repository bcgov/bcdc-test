# Overview

The ckan scheming extension allows for the publishing of the data schema that is 
being used by ckan.  For testing we want to be able to consume the scheming end 
point and use it to generate dynamically test data.

The module create_bcdc_dataset will consume the data returned by the scheming
extension and then dynamically generate test data.

# Generated Test Data

## Simple bcdc_dataset

Initially will develop methods that will generate bcdc_dataset with:
 - required fields
 - all fields.

These tests will then be factored into the parameterization allowing for us to 
run tests with dynamically generated data.

## Required Field Verification

These tests will iterate over the required fields for a bcdc_dataset, for each 
iteration it will remove one of the required fields.  This data can be thrown 
at the Create tests to verify that they fail when missing a field.

## Choice Field Verification

Add tests to iterate through the domains defined for choice fields to verify that 
they are correct.

## Field types

Some fields contain a value called "preset" that defines the type of data that 
is expected for that field.  A list of possible values includes:

* autocomplete
* composite
* composite_repeating
* dataset_organization
* dataset_slug
* date
* json_object
* resource_url_upload
* select
* tag_string_autocomplete
* title
