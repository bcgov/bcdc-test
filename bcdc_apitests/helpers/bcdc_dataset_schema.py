'''
Created on Sept 13, 2019

@author: KJNETHER

This module contains functionality that can be used to consume the scheming
end points.  Population module will use

uses the data from scheming end point to construct datasets

Things to think about:
 - orgs used to construct the data set should be passed as args
        visibility is NOT impacted by org.
 - publish_state: Type of data ['DRAFT', 'PUBLISHED', 'PENDING ARCHIVE',
                               'REJECTED', 'PENDING PUBLISHED']
     are likely suppose to exhibit different behavior, need to code that in
 - 'metadata_visibility': test visibility of data this will impact visibility

 admin - only admin can see published.
 logged in become 'gov' not logged in 'not gov'


 # example end point for scheming data:
 https://cadi.data.gov.bc.ca/api/3/action/scheming_dataset_schema_show?type=bcdc_dataset

'''
# TODO: conditional_fields are not working right now, should only get populated
#       if the condition is true
# TODO: modify so that extent populates with a lat long values.  Will do this for
#       any fields names that satisfy regular expression *latitude* *longitude*

import json
import logging
import os

import bcdc_apitests.config.testConfig as testConfig
import bcdc_apitests.helpers.file_utils as file_utils

# pylint: disable=logging-fstring-interpolation

LOGGER = logging.getLogger(__name__)


class Fields():
    '''
    abstraction of fields in general that can be used with both 'dataset_fields'
    and 'resource_fields'

    expects the data structure that is passed to the constructor to be a list
    '''

    def __init__(self, struct):
        self.struct = struct
        self.all_flds = []
        # filtered_list if populated will be used for iterators.  If its set to
        # none then iterators will use all_flds
        self.filtered_list = None
        self.itercnt = 0
        self.__parse_flds()

    def set_field_type_filter(self, property_name=None, property_value=None):
        '''
        This method can be used to set a filter.  The filter will restrict the
        types of fields that will be provided to the iterator.  Example of usage

        if you only want fields where 'required' = true

        :param property_name: the name of the property that you want to add a
                              filter to.  If set to none it will clear
                              any existing filters
        :param property_value: the name of the value that corresponds with the
                              property_name for setting the filter.

        If called twice will perform an Or condition for previous calls to the
        filter, ie included in set if condition1 or condition2 are met.

        Haven't needed and yet so haven't implemented.
        '''
        if property_name is None:
            self.filtered_list = None
        else:
            if self.filtered_list is None:
                self.filtered_list = []
            for fld in self:
                val = fld.get_value(property_name)
                if (val is not None) and val == property_value:
                    self.filtered_list.append(fld)

    def __parse_flds(self):
        '''
        Reads the json struct and uses it to create a list of individual
        Field objects stored in the property all_flds
        '''
        self.all_flds = []
        for fld_data in self.struct:
            fld = Field(fld_data)
            self.all_flds.append(fld)
        self.current_list = None

    def __iter__(self):
        '''
        implement iterator
        '''
        self.itercnt = 0
        return self

    def __next__(self):
        '''
        Iterator:
        If a filter is defined then iterate over the filtered list,
        otherwise iterate over all_flds
        '''
        iter_list = self.all_flds
        if self.filtered_list is not None:
            iter_list = self.filtered_list
        if self.itercnt >= len(iter_list):
            raise StopIteration

        return_value = iter_list[self.itercnt]
        self.itercnt += 1
        return return_value

    def reset(self):
        '''
        resets the iterator
        '''
        self.itercnt = 0


class CKANCorePackage(Fields):
    '''
    The CKAN Scheming extension defines a json schema that can be used to
    describe custom data models used by CKAN extensions.  A file has been created
    that uses the scheming extension to describe the core fields for packages.

    This class is configured to read that file.  The BCDCDataset class will
    then subclass / extend this class.
    '''

    def __init__(self, dataset_type, struct=None):
        # the schema for ckan core packages is not available via an end point.  its
        # a static json file has been created to describe it using the schema
        # json data model.
        # valid types:
        valid_data_types = ['dataset_fields', 'resource_fields', 'subfields']
        if dataset_type not in valid_data_types:
            # throw error
            # TODO: should define a custom error
            msg = f'CKANCorePackage constructor dataset_type: {dataset_type}' + \
                  f'is an invalid, valid values include: {valid_data_types}'
            raise ValueError(msg)

        if struct is None:
            struct = self.__get_ckan_core_schema(dataset_type)
        LOGGER.debug(f"CKANCorePackage core struct: {struct}")
        Fields.__init__(self, struct)
        self.all_flds = []
        self.__parse_flds()
        LOGGER.debug(f"CKANCoreFields: self.all_flds: {self.all_flds}")

    def __get_ckan_core_schema(self, data_type):
        '''
        The ckan scheming definition for the core ckan fields does not exist.
        The test suite has one defined in the 'test_data' directory.  This
        method will calculate the path to that file, open it, read the json
        into a python data structure, and return that data structure
        '''
        fu = file_utils.FileUtils()
        data_dir = fu.get_test_data_dir()
        schema_file = testConfig.TEST_CKAN_CORE_SCHEMA_DEF
        schema_file_full_path = os.path.join(data_dir, schema_file)

        fh = open(schema_file_full_path, 'r')
        schematext = fh.read()
        fh.close()
        data_struct = json.loads(schematext)
        # if isinstance(data_struct, list):
        #    return_value = data_struct
        if data_type in data_struct:
            return_value = data_struct[data_type]
        else:
            return_value = []
        return return_value

    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.all_flds = []
        for fld_data in self.struct:
            fld = CKANCoreField(fld_data)
            # if fld.is_required():
            self.add_field(fld)
            # self.all_flds.append(fld)
        self.current_list = None

    def get_presets(self, start_list=None):
        '''
        Used to validate the expected values in the presets with what the tests
        are configured to consume.

        :param start_list: Used to allow for recursion, by default iterates over
                         the fields in the root portion of the json struct, if
                         a subfield is encountered, calls itself with the subfield
                         data.

        :returns: a unique list of preset values found in the schema
        '''
        preset = []
        if start_list is None:
            start_list = self.struct
        for fld in self:
            if fld.preset:
                preset.append(fld.preset)
            elif fld.has_fld('subfields'):
                preset.extend(self.get_presets(fld['subfields']))
        return list(set(preset))

    def get_field_names(self):
        '''
        :return: a list of the field names that are defined for this schema.  Does
                 not include subfields
        '''
        fld_names = []
        for fld in self:
            fld_names.append(fld.field_name)
        return fld_names

    def field_exists(self, field):
        exists = False
        for fld in self:
            if fld.field_name == field.field_name:
                exists = True
                break
        return exists

    def field_name_exists(self, field_name):
        '''
        :param field_name: input field name
        :return: boolean depending on whether the schema includes a definition
            for the input field_name
        '''
        field_names = self.get_field_names()
        ret_val = False
        if field_name in field_names:
            ret_val = True
        return ret_val

    def remove_field(self, field):
        '''
        if the field exists it is removed
        '''
        removed = False
        fldcnt = 0
        for fld in self.all_flds:
            if fld.field_name == field.field_name:
                removed = True
                break
            fldcnt += 1
        if removed:
            del self.all_flds[fldcnt]
        return removed

    def add_field(self, field):
        '''
        checks to see if a field already exists, if it does it gets removed
        and replaced with the new one, otherwise the field is added
        '''
        was_removed = self.remove_field(field)
        LOGGER.debug(f"removed the field?: {was_removed}")
        self.all_flds.append(field)

    def get_field(self, field_name):
        '''
        :return: a field object for the field that corresponds with the field
                 name provided... returns None if the field does not exist.
        '''
        field = None
        for fld in self:
            LOGGER.debug(f'field name: {fld.field_name}')
            if fld.field_name == field_name:
                field = fld
                break
        return field


class BCDCDataset(CKANCorePackage):
    '''
    extends generic Fields with specific code to Dataset Fields
    '''

    def __init__(self, struct, dataset_type=None):
        CKANCorePackage.__init__(self, dataset_type=dataset_type)
        self.dataset_type = dataset_type
        self.struct = struct
        self.__parse_flds()

    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        # self.all_flds = []
        for fld in self.all_flds:
            LOGGER.debug(f"existing field: {fld.field_name}")
        LOGGER.debug(f'struct: {self.struct}')
        LOGGER.debug(f'self.dataset_type: {self.dataset_type}')
        for fld_data in self.struct[self.dataset_type]:
            LOGGER.debug(f"fld_data: {fld_data}")
            fld = BCDCDatasetField(fld_data)
            LOGGER.debug(f"adding fields {fld.field_name}.")
            # if fld.is_required():
            # self.all_flds.append(fld)
            self.add_field(fld)


class Field():
    '''
    Simple implemenation of a field.  Does not contain individual
    field implemenation.
    '''

    def __init__(self, fld):
        self.fld = fld

    def has_fld(self, property_name):
        '''
        :return: true or false if the field has this property
        '''
        has_fld = False
        if property_name in self.fld:
            has_fld = True
        return has_fld

    def fld_is_true(self, fld_name):
        '''
        Identifies if the field exists AND is set to True
        :param fld_name: input field name
        '''
        fld_true = False
        if (self.has_fld(fld_name)) and self.fld[fld_name]:
            fld_true = True
        return fld_true

    def get_value(self, property_name):
        '''
        :param property_name:  retrieves the value for corresponding
            property_name.  If the property_name is not defined for this field
            then returns None.
        '''
        val = None
        if self.has_fld(property_name):
            val = self.fld[property_name]
        return val

    def __str__(self):
        '''
        implementing built-in for this object
        '''
        outlist = []
        for i in self.fld:
            # LOGGER.debug(f"i: {i}")
            # LOGGER.debug(f"i: {self.fld[i]}")
            outlist.append(f'{i} : {self.fld[i]}')
        outstr = ', '.join(outlist)
        return outstr


class CKANCoreField(Field):
    '''
    reads the core ckan fields, this class can then be inherited by the bcdc_dataset
    schema.
    '''

    def __init__(self, fld):
        Field.__init__(self, fld)
        self.default_preset = 'string'

    @property
    def required(self):
        '''
        making required a property
        '''
        return self.fld_is_true('required')

    @property
    def has_choices(self):
        '''
        creating a property for has_choices, used to determine if
        the field has a choices property.
        '''
        return self.has_fld('choices')

    @property
    def field_name(self):
        '''
        :return: the field name
        '''
        return self.fld['field_name']

    @property
    def choices(self):
        '''
        :return: a Fields object with the choice options
        '''
        retval = None
        if self.has_choices:
            retval = Choices(self.fld['choices'])
        return retval

    @property
    def has_subfields(self):
        '''
        :return: the value for subfields if it exists, otherwise None
        '''
        return self.has_fld('subfields')

    @property
    def subfields(self):
        '''
        :return: a 'Fields' object with the contents of the subfields
        '''
        # return BCDCDataset(self.fld['subfields'], dataset_type='subfields')
        LOGGER.debug(f"processing subfields: {self.fld['subfields']}")
        struct = {}
        struct['subfields'] = self.fld['subfields']
        return BCDCDataset(struct, dataset_type='subfields')

    @property
    def preset(self):
        '''
        :return: the value for the property preset, if it is not defined it will
                 be set to the default preset value defined in the class.
        '''
        preset_value = self.get_value('preset')
        if not preset_value:
            preset_value = self.default_preset
        return preset_value

    @property
    def choices_helper(self):
        '''
        :return: the contents of the choices_helper field
        '''
        return self.get_value('choices_helper')

    @property
    def conditional_field(self):
        '''
        :return: the value of the conditional_field for this field
        '''
        return self.get_value('conditional_field')

    @property
    def conditional_values(self):
        '''
        :return: the value of the conditional_values for this field
        '''
        return self.get_value('conditional_values')


class BCDCDatasetField(CKANCoreField):
    '''
    a wrapper for individual field objects.  Provides quick access to properties
    of the field
    '''

    def __init__(self, fld):
        CKANCoreField.__init__(self, fld)


class Choices():
    '''
    a wrapper for "Choices" associated with various fields.
    '''

    def __init__(self, choice_struct):
        self.choice_struct = choice_struct
        self.choices = []
        self.__parse()
        LOGGER.debug(f"choices data: {choice_struct}")

    def __parse(self):
        '''
        reads the json struct and makes pieces of it available through this
        class.
        '''
        for choice_data in self.choice_struct:
            self.choices.append(Choice(choice_data))

    @property
    def values(self):
        '''
        :return: a list of the possible values for this choice field, other
            words the domain.
        '''
        LOGGER.debug("values called")
        value_list = []
        for choice in self.choices:

            value_list.append(choice.value)
        return value_list

    def __len__(self):
        '''
        override python built-in for length
        '''
        return len(self.choice_struct)


class Choice(Field):
    '''
    a wrapper class for individual choices that make up
    Choices objects
    '''

    def __init__(self, choice_data):
        Field.__init__(self, choice_data)
        self.choice_data = choice_data

    @property
    def value(self):
        '''
        :return: the value for this choice
        '''
        return self.get_value('value')
