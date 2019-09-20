'''
Created on Sept 13, 2019

@author: KJNETHER

uses the data from scheming end point to construct datasets

Things to think about:
 - orgs used to construct the data set should be passed as args
 - Type of data ['DRAFT', 'PUBLISHED', 'PENDING ARCHIVE', 'REJECTED', 'PENDING PUBLISHED']
     are likely suppose to exhibit different behavior, need to code that in
 - 

'''
import logging
import json
import os
import random_word

import random

import bcdc_apitests.helpers.data_config as data_config
import bcdc_apitests.config.testConfig as testConfig

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
            self.current_list = None
        else:
            if self.current_list is None:
                self.current_list = []
            for fld in self:
                val = fld.get_value(property_name)
                if (val is not None) and val == property_value:
                    self.current_list.append(fld)

    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.required_flds = []
        self.optional_flds = []
        self.all_flds = []
        for fld_data in self.struct:
            fld = Field(fld_data)
            self.all_flds.append(fld)
        self.current_list = None

    # DELETE this method, should be move to the population class
#     def get_fields(self, field_list=None):
#         '''
#         :param field_list: the list of field objects to be processed.
#
#         For each field object we need:
#          - a field name
#          - a field value (dummy value)
#
#         if the field type is choice, the the value needs to come from
#         the list of choices.
#
#         if the field type is a subfield and the preset is "composite_repeating"
#         then the field value will be a list, and the component fields will be
#         a list of "field name", field value pairs
#
#
#         '''
#         if field_list is None:
#             field_list = self.all_flds
#
#         output_dataset = {}
#         for fld in field_list:
#             if fld.has_choices:
#                 value = fld.choices.get_random_value()
#                 output_dataset[fld.field_name] = value
#             elif fld.has_subfields:
#                 output_dataset[fld.field_name] = []
#                 self.get_fields(fld.subfields)

    def __iter__(self):
        self.itercnt = 0
        return self

    def __next__(self):
        '''
        If a filter is defined then iterate over the filtered list,
        otherwise iterate over all_flds
        '''
        iterList = self.all_flds
        if self.filtered_list is None:
            iterList = self.all_flds
        if self.itercnt >= len(iterList):
            raise StopIteration
        else:
            return_value = iterList[self.itercnt]
            self.itercnt += 1
            return return_value

    def reset(self):
        '''
        resets the iterator
        '''
        self.itercnt = 0


class DatasetFields(Fields):
    '''
    extends generic Fields with specific code to Dataset Fields
    '''

    def __init__(self, struct):
        Fields.__init__(self, struct)
        self.required_flds = []
        self.optional_flds = []
        self.__parse_flds()

    def get_presets(self, startList=None):
        '''
        Used to validate the expected values in the presets with what the tests
        are configured to consume.

        :param startList: Used to allow for recursion, by default iterates over
                         the fields in the root portion of the json struct, if
                         a subfield is encountered, calls itself with the subfield
                         data.

        :returns: a unique list of preset values found in the schema
        '''
        preset = []
        if startList is None:
            startList = self.struct
        for fld in self:
            if fld.preset:
                preset.append(fld.preset)
            elif fld.has_fld('subfields'):
                preset.extend(self.get_presets(fld['subfields']))
        return list(set(preset))

    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.required_flds = []
        self.optional_flds = []
        self.all_flds = []
        for fld_data in self.struct:
            fld = DatasetField(fld_data)
            # if fld.is_required():
            if fld.required:
                self.required_flds.append(fld)
            else:
                self.optional_flds.append(fld)
            self.all_flds.append(fld)
        self.current_list = None


class Field():
    '''
    Simple implemenation of a field.  Does not contain individual
    field implemenation.
    '''

    def __init__(self, fld):
        self.fld = fld

    def has_fld(self, fldname):
        has_fld = False
        if (fldname in self.fld):
            has_fld = True
        return has_fld

    def fld_is_true(self, fld_name):
        '''
        Identifies if the field exists AND is set to True
        :param fld_name: input field name
        '''
        fld_true = False
        if (self.has_fld(fld_name)) and  self.fld[fld_name] == True:
            fld_true = True

    def get_value(self, property):
        '''
        :param property:  retrieves the value for corresponding property.  If the property is
        not defined for this field then returns None.
        '''
        val = None
        if self.has_fld(property):
            val = self.fld[property]
        return val

    def __str__(self):
        outlist = []
        for i in self.fld:
            # LOGGER.debug(f"i: {i}")
            # LOGGER.debug(f"i: {self.fld[i]}")
            outlist.append(f'{i} : {self.fld[i]}')
        outstr = ', '.join(outlist)
        return outstr


class DatasetField(Field):
    '''
    a wrapper for individual field objects.  Provides quick access to properties
    of the field
    '''

    def __init__(self, fld):
        Field.__init__(self, fld)

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
        return DatasetFields(self.fld['subfields'])

    @property
    def preset(self):
        '''
        :return: the value for the property preset, or None if its not defined
        '''
        return self.get_value('preset')

#     @property
#     def test_value(self):
#         '''
#         returns a random test value for the field that matches the type that
#         is defined in the schema for the field.
#
#         type is based on the 'preset' value.  If no preset is provided then
#         assume the type is string
#         '''
#         # TODO: Delete method, once logic has been moved to a populate class
#         if self.choices:
#             test_value = choices.get_random_value()
#         elif self.has_subfields:
#             pass


class DataPopulation():
    '''
    This class uses Fields objects, iterates over the fields objects populating
    the fields objects with data.
    '''

    def __init__(self, fields):
        # TODO: may want to pass in the organization to put the data under
        self.fields = fields
        self.datastruct = {}

    def populate_all(self):
        '''
        iterates over the fields object populating it with data.

        data population will be different for different preset types.

        Current list of presets:
            * autocomplete - treated same as choice
            * composite    - has subfields, a list of dicts
            * composite_repeating - has subfields, the schema repeats, for the list
            * dataset_organization - the reference to an existing org, for now hardcoding test-organization
            * dataset_slug - used for name of the package
            * date - looks like YY-MM-DD 2019-06-13
            * json_object - not required, skipping for now
            * resource_url_upload - not required, not sure skip
            * select -  another choice... select one.
            * tag_string_autocomplete - might come from tags?
            * title - just text

        This method will populate all the fields defined in the schema, except
        types noted above
        '''
        datastruct = {}
        # set the scope for this variable for this method
        fld = None
        def undefined_prefix(fld):
            msg = f'prefix is set to: {fld.preset}.  There is no code to ' + \
                  'to accomodate this type.  Need to add a method definition for ' + \
                  'that type to this class'
            raise UndefinedPrefix(msg)

        for fld in self.fields:
            # population is based on the preset, if no preset available then
            # assume str
            LOGGER.debug(f'Fld is: {fld}')
            LOGGER.debug(f'Fld preset is: {fld.preset}')
            if fld.preset is None:
                field_value = self.string(fld)
            else:
                # the name of the method to call is contained in the property: preset,
                # turning the value of preset into a method call
                func = getattr(self, fld.preset, undefined_prefix)
                field_value = func(fld)
            datastruct[fld.field_name] = field_value
        return datastruct

    def select(self, fld):
        
        LOGGER.debug(f" Calling SEELCTfld: {fld}")
        
        LOGGER.debug(f" number of choices: {len(fld.choices)}")
        values = fld.choices.values
        LOGGER.debug(f" values: {values}")
        value = values[random.randint(0, len(values) - 1)]
        return value
    
    def title(self, fld):
        '''
        sets the title for the data set, going to hard code this as 
        test_data
        '''
        return data_config.DataSetValues.title
    
    def dataset_slug(self, fld):
        '''
        This is currently configured for the name of the dataset to just returning
        the name of the dataset.
        '''
        return testConfig.TEST_PACKAGE
    
    def dataset_organization(self, fld):
        '''
        :returns: retrieves the name of the organization that is going to be 
                 used by the testing and returns it
        '''
        return testConfig.TEST_ORGANIZATION
    
    def string(self, fld):
        rand = random_word.RandomWords()

        word = rand.get_random_word()
        return word
    
    def tag_string_autocomplete(self, fld):
        '''
        Not sure if this should be referencing existing tags... for now
        just making it random text.
        '''
        return self.string(fld)
        
    def composite_repeating(self, fld):
        '''
        This type of field is a list made up of a bunch of subfields, this 
        call will make a couple calls to this Datapopulation class to generate
        new subfields
        '''
        for subfield in fld.subfields():
            pass
        


class DataSet():
    '''
    A container where simple fields with name and value pairs can be added.
    '''

    def __init__(self):
        fields = []
        subfields = {}

    def addfield(self, name, value):
        fld_dict = {'field_name': name,
                    'field_value': value}

#     def addsubfield(self, name, value):
#         '''
#         :param name: the name of the subfield to be added
#         :param value: a list of values that comply with the schema, not validated
#                       here, this is only a simple method that allows you to add
#                       new
#         '''


class Choices():

    def __init__(self, choice_struct):
        self.choice_struct = choice_struct
        self.choices = []
        self.__parse()
        LOGGER.debug(f"choices data: {choice_struct}")

    def __parse(self):
        for choice_data in self.choice_struct:
            self.choices.append(Choice(choice_data))

    @property
    def values(self):
        LOGGER.debug("values called")
        value_list = []
        for choice in self.choices:
            
            value_list.append(choice.value)
        return value_list

    def __len__(self):
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

        '''
        return self.get_value('value')


class UndefinedPrefix(AttributeError):

    def __init__(self, message, errors=None):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        pass


if __name__ == '__main__':
    # dev work... eventually will have data come from the api end point
    # read data from canned example of data_schema
    dataSchemaFile = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'data_schema.json')
    fh = open(dataSchemaFile, 'r')
    schematext = fh.read()
    fh.close()
    data_struct = json.loads(schematext)

    # simple logging setup
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    hndlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)
    LOGGER.debug("test")

    # get the possible preset values
    # # presets for datasets
    bcdc_dataset = DatasetFields(data_struct['dataset_fields'])
    presets = bcdc_dataset.get_presets()
    # # presets for resources
    resources = DatasetFields(data_struct['resource_fields'])
    resource_preset = resources.get_presets()
    presets.extend(resource_preset)  # combine presets
    presets = list(set(presets))
    presets.sort()
    LOGGER.debug(f'presets: {presets}')
    # TODO: should add methods to validate the returned schema.  Testing is expecting a subset of presets, should make sure that the presets in the data match what is expected if not then throw a useful error message.

    # retrieve the required fields
    bcdc_dataset.set_field_type_filter('required', True)
    for fld in bcdc_dataset:
        fld_nm = fld.get_value('field_name')
        LOGGER.debug(f"field_name: {fld_nm}, {fld.preset}")

    populator = DataPopulation(bcdc_dataset)
    populator.populate_all()

