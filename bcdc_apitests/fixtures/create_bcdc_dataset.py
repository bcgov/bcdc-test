'''
Created on Sept 13, 2019

@author: KJNETHER

uses the data from scheming end point to construct datasets

'''
import logging
import json
import os
import random
from builtins import None
from pylint.test.functional.unpacking_non_sequence import IterClass



LOGGER = logging.getLogger(__name__)
        
                
           
class Fields(object):
    '''
    abstraction of fields in general that can be used with both 'dataset_fields'
    and 'resource_fields'
    
    expects the data structure that is passed to the constructor to be a list
    '''
    
    def __init__(self, struct):
        self.struct = struct
        self.required_flds = []
        self.optional_flds = []
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
                    self.current_list.append()
        
    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.required_flds = []
        self.optional_flds = []
        self.all_flds = []
        for fld_data in self.struct:
            fld = Field(fld_data)
            #if fld.is_required():
            if fld.required:
                self.required_flds.append(fld)
            else:
                self.optional_flds.append(fld)
            self.all_flds.append(fld)
        self.current_list = None
                
    # DELETE this method, should be move to the population class
    def get_fields(self, field_list=None):
        '''
        :param field_list: the list of field objects to be processed.
        
        For each field object we need:
         - a field name
         - a field value (dummy value)
         
        if the field type is choice, the the value needs to come from 
        the list of choices.
        
        if the field type is a subfield and the preset is "composite_repeating"
        then the field value will be a list, and the component fields will be 
        a list of "field name", field value pairs
                       
        
        '''
        if field_list is None:
            field_list = self.all_flds
        
        output_dataset = {}
        for fld in field_list:
            if fld.has_choices:
                value = fld.choices.get_random_value()
                output_dataset[fld.field_name] = value
            elif fld.has_subfields:
                output_dataset[fld.field_name] = []
                self.get_fields(fld.subfields)
        
    # DELETE, not requires
    def get_required_fields(self):
        '''
        Generates a list of simplified data fields where each datafield only
        contains name, value pairs.  If the field is a composite field it will 
        be equal to a list of name, value pairs.
        '''
        output_dataset = {}
        for fld in self.required_flds:
            if fld.has_choices:
                value = fld.choices.get_random_value()
                output_dataset[fld.field_name] = value
            elif fld.has_subfields:
                output_dataset[fld.field_name] = []
                subflds = fld.subfields

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
            elif 'subfields' in fld:
                preset.extend(self.get_presets(fld['subfields']))         
        return list(set(preset))
    
    def __iter__(self):
        self.itercnt = 0
        return self
    
    def __next__(self):
        '''
        If a filter is defined then iterate over the filtered list, 
        otherwise iterate over all_flds
        '''
        iterList = self.all_flds
        if filtered_list is None:
            iterList = all_flds
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
        
        
                
class Field(object):
    '''
    a wrapper for individual field objects.  Provides quick access to properties
    of the field
    '''
    
    def __init__(self, fld):
        self.fld = fld
        
    def is_required(self):
        is_required = False
        if ('required' in self.fld) and self.fld['required'] == True:
            is_required = True
    
    def has_fld(self, fldname):
        has_fld = False
        if (fldname in self.fld):
            has_fld = True
        return has_fld
    
    def fld_is_true(self, fld_name):
        fld_true = False
        if (self.has_fld(fld_name)) and  self.fld[fld_name] == True:
            fld_true = True
    
    def get_value(self, property):
        '''
        retrieves the value for corresponding property.  If the property is 
        not defined for this field then returns None.
        '''
        val = None
        if (self.has_fld(property)):
            val = self.fld[property]
        return val
    
    @property    
    def required(self):
        return self.fld_is_true('required')
    
    @property
    def has_choices(self):
        return self.has_fld('choices')
    
    @property
    def field_name(self):
        return self.fld['field_name']
    
    @property
    def choices(self):
        '''
        :return: a Fields object with the choice options
        '''
        return Choices(self.fld['choices'])
    
    @property
    def has_subfields(self):
        return self.has_fld('subfields')
    
    @property
    def subfields(self):
        '''
        Iterates over each of the subfields and returns as Fields object
        '''
        return Fields(self.fld['subfields'])
    
    @property
    def preset(self):
        return self.get_value('preset')
        
    @property
    def test_value(self):
        '''
        returns a random test value for the field that matches the type that 
        is defined in the schema for the field.
        
        type is based on the 'preset' value.  If no preset is provided then 
        assume the type is string
        '''
        if self.has_choices:
            test_value = choices.get_random_value()
        elif self.has_subfields:
            pass
      
class DataPopulation(object):
    '''
    This class uses Fields objects, iterates over the fields objects populating 
    the fields objects with data.
    '''
    def __init__(self, fields):
        self.fields = fields
        self.datastruct = {}
    
    def populate(self):
        '''
        iterates over the fields object populating it with data.
        '''
        for fld in self.fields
      
            
class DataSet(object):
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
        
        
    
    
class Choices(object):
    def __init__(self, choice_struct):
        self.choice_struct = choice_struct
        self.choices = []
    
    def __parse(self):
        for choice_data in self.choice_struct:
            self.choices.append(Choice(choice_data))
                  
    @property
    def values(self):
        value_list = []
        for choice in choices:
            value_list.append(choice.value)
        return value_list
    
    def get_random_value(self):
        '''
        :return: a random value that is defined for this choices domain
        '''
        return self.values[random.randint(0, len(self.values))]
        

class Choice(object):
    def __init__(self, choice_data):
        self.choice_data = choice_data
        
    @property
    def value(self):
        return self.choice_data['value']
            
class BCDCDataset(Fields):
    def __init__(self, bcdc_dataset_struct):
        Fields.__init__(self, bcdc_dataset_struct)
        
        
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
    ## presets for datasets
    bcdc_dataset = BCDCDataset(data_struct['dataset_fields'])
    presets = bcdc_dataset.get_presets()
    ## presets for resources
    resources = BCDCDataset(data_struct['resource_fields'])
    resource_preset = resources.get_presets()
    presets.extend(resource_preset) #combine presets
    presets = list(set(presets))
    presets.sort()
    LOGGER.debug(f'presets: {presets}')
    # TODO: should add methods to validate the returned schema.  Testing is expecting a subset of presets, should make sure that the presets in the data match what is expected if not then throw a useful error message.
    
    # retrieve the required fields
    bcdc_dataset.get_required_fields()
    
    