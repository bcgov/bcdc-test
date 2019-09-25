'''
Created on Sept 13, 2019

@author: KJNETHER

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

import datetime
import json
import logging
import os
import random

import randomwordgenerator.randomwordgenerator

import bcdc_apitests.config.testConfig as testConfig
import bcdc_apitests.helpers.data_config as data_config

# pylint: disable=logging-fstring-interpolation

LOGGER = logging.getLogger(__name__)

# module wide access to random words.
WORDS = []


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

    def __init__(self, struct):
        Fields.__init__(self, struct)
        self.all_flds = []
        self.__parse_flds()

    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.all_flds = []
        for fld_data in self.struct:
            fld = CKANCoreField(fld_data)
            # if fld.is_required():
            self.all_flds.append(fld)
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


class BCDCDataset(CKANCorePackage):
    '''
    extends generic Fields with specific code to Dataset Fields
    '''

    def __init__(self, struct, dataset_type=None):
        CKANCorePackage.__init__(self, struct)
        self.__parse_flds()
        self.dataset_type = dataset_type

    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.all_flds = []
        for fld_data in self.struct:
            fld = BCDCDatasetField(fld_data)
            # if fld.is_required():
            self.all_flds.append(fld)
        self.add_type()

    def add_type(self):
        '''
        Dataset type is not included as a field definition in dataset_fields,
        the type can be passed to the constructor though.  dataset_type is a required
        field as other fields identify it as a conditional field.
        '''
        field_struct = { "field_name": "dataset_type",
                        "label": "dataset type",
                        "required": True }
        fld = BCDCDatasetField(field_struct)
        self.all_flds.append(fld)


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
        return BCDCDataset(self.fld['subfields'])

    @property
    def preset(self):
        '''
        :return: the value for the property preset, or None if its not defined
        '''
        return self.get_value('preset')

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


class RandomWords():
    '''
    The module I was using for random words makes a network call, which is slow
    so wrapping it with this module so that it makes one network call and caches
    100 random words, once the 100 are used up it will grab another 100, hopeuflly
    speeding things up.
    '''

    def __init__(self, cache_size=500):
        self.cache_size = cache_size
        # self.words = []

    def getword(self):
        '''
        :return: a random word that can be used for various fields.
        '''
        global WORDS  # pylint: disable=global-statement
        if not WORDS:
            self.get_words_from_network()
        return WORDS.pop()

    def get_words_from_network(self):
        '''
        Goes to the network, and reloads the cache with the number of words
        defined in the cache_size.
        '''
        LOGGER.info(f"getting another {self.cache_size} random words" +  # pylint: disable=logging-not-lazy
                    "from generator..")
        # can't think of a way around this, want to make the WORDS available to
        # all instances of the module
        global WORDS  # pylint: disable=global-statement
        WORDS = randomwordgenerator.randomwordgenerator.generate_random_words(
            self.cache_size)


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


class DataPopulation():
    '''
    Each of these methods can be used to generate either:
      - an iterable object where each iteration returns a single dataset
      - a single dataset.

    The names of the methods from this class can be identified in the
    parameterization, along with:
      - the user type they should be run under
      - The tests that the data should be used with
      - The expected outcome
    '''

    def __init__(self):
        # Construct a , BCDCDataset
        #
        pass

    def create_BCDC_dataset(self):
        '''
        - hits the end point for scheming,
        - uses the scheming struct to construct a BCDCDataset for the dataset_fields
        - use the BCDCDataset and methods in DataPopulationResource to create an
          example record.
        '''
        pass


class DataPopulationResource():
    '''
    This class contains re-usable functionality that can be used to assemble
    methods in the DataPopulation class.

    Idea is the publicly accessible methods in DataPopulation will be included
    in the parameterization.  Those methods will use functionality in this class
    to accomplish what they need to do.
    '''

    def __init__(self, fields):
        # TODO: may want to pass in the organization to put the data under
        self.fields = fields
        LOGGER.debug(f"type of fields: {type(fields)}")
        # TODO: use isinstance to enforce type here maybe... should be Fields or
        # subclass of.
        self.datastruct = {}
        self.rand = RandomWords()
        self.deferred = []

    def has_conditional(self, fld):  # pylint: disable=no-self-use
        '''
        :return: true if the field has a conditional property
        '''
        has_cond = False
        if fld.conditional_field:
            has_cond = True
        return has_cond

    def conditional_field_exists(self, fld):
        '''
        :return: true if the field has a conditional field and the conditional
                 field exists in the fields that have already been processed.
        '''
        cond_exists = False
        if (self.has_conditional) and fld.conditional_field in self.datastruct:
            cond_exists = True
        return cond_exists

    def conditional_satisfied(self, fld):
        '''
        :param fld: a Field object.

        * does the fld have a condition, if not then return True, proceed.

        * otherwise...

        * if conditional_field exists, then determine the value and populate
          field of value matches conditional value.
            * if condition is met then True
            * otherwise False

        * if the conditional_field does not exist, then add to the deferred
          processing.
            * return False
        '''
        proceed = False
        # field exists in the populated dataset, and the value of the field
        # in the populated dataset matches the condition
        if (self.conditional_field_exists(fld)) and \
           self.datastruct[fld.conditional_field] in fld.conditional_values:
            LOGGER.debug(f"conditional satisfied: {fld.conditional_field}, " +
                         f"{self.datastruct[fld.conditional_field]}, " +
                         f"{fld.conditional_values}")
            proceed = True
        LOGGER.debug(f"conditional_satisfied return: {proceed}")
        return proceed

    def populate_all(self):
        '''
        iterates over the fields object populating it with data.

        data population will be different for different preset types.

        Current list of presets:
            * autocomplete - treated same as choice
            * composite    - has subfields, a list of dicts
            * composite_repeating - has subfields, the schema repeats, for the
                                    list
            * dataset_organization - the reference to an existing org, for now
                                    hard coding test-organization
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
        # datastruct = {}
        # set the scope for this variable for this method
        fld = None

        def undefined_prefix(fld):
            msg = f'prefix is set to: {fld.preset}.  There is no code to ' + \
                  'to accomodate this type.  Need to add a method definition for ' + \
                  'that type to this class'
            raise UndefinedPreset(msg)

        for fld in self.fields:
            # population is based on the preset, if no preset available then
            # assume str
            LOGGER.debug(f'Fld is: {fld}')
            LOGGER.debug(f'Fld preset is: {fld.preset}')

            # Does the field have a conditional property AND the conditional resolves as False...
            if self.has_conditional(fld) and not self.conditional_satisfied(fld):
                # condition is not met, add to deferred
                LOGGER.debug(f"adding to the deferred list: {fld}")
                self.deferred.append(fld)
            else:
                if fld.preset is None:
                    field_value = self.string(fld)
                else:
                    # the name of the method to call is contained in the property: preset,
                    # turning the value of preset into a method call
                    func = getattr(self, fld.preset, undefined_prefix)
                    field_value = func(fld)
                self.datastruct[fld.field_name] = field_value
        if self.deferred:
            self.process_deferred_fields()
            # shortcut for now... should really continuously iterate through deferred
            # fields until they are all removed
        return self.datastruct

    def process_deferred_fields(self):
        '''
        Some fields like
        '''
        LOGGER.debug(f"deferred: {len(self.deferred)} {self.deferred}")
        if self.deferred:
            to_remove = []
            for defer_cnt in range(0, len(self.deferred)):
                defer_fld = self.deferred[defer_cnt]
                LOGGER.debug(f"processing deferred field: {defer_fld}")
                # conditional exists, therefore can retrieve its value
                if self.conditional_field_exists(defer_fld):
                    LOGGER.debug(f"conditional field exists: {defer_fld}")
                    # is the condition satisfied
                    if self.conditional_satisfied(defer_fld):
                        if defer_fld.preset is None:
                            field_value = self.string(defer_fld)
                        else:
                            # the name of the method to call is contained in the property: preset,
                            # turning the value of preset into a method call
                            func = getattr(self, defer_fld.preset)
                            field_value = func(defer_fld)
                        self.datastruct[defer_fld.field_name] = field_value
                        to_remove.append(defer_fld)
                    else:
                        # conditional field exists, but the condition is not
                        # satisfied, don't populate, and remove from deferred list
                        if defer_fld.field_name in self.datastruct:
                            del self.datastruct[defer_fld.field_name]
                        to_remove.append(defer_fld)
            # after iteration remove the deferred fields, then try again
            for remove_rec in to_remove:
                self.deferred.remove(remove_rec)
            self.process_deferred_fields()

    def select(self, fld):
        '''
        used for preset "select", grabs a random value from the choices option.

        Future: some fields may need the ability to select multiple values.
        '''
        LOGGER.debug(f" Calling Select on fld: {fld}")
        if fld.choices:
            LOGGER.debug(f" number of choices: {len(fld.choices)}")
            values = fld.choices.values
            LOGGER.debug(f" values: {values}")
            value = values[random.randint(0, len(values) - 1)]
        elif (fld.choices_helper) and fld.choices_helper == 'edc_orgs_form':
            # TODO, example of this is the subfield for contacts...
            #   field_name = org
            # add a edc_org used for the package
            value = self.dataset_organization(fld)
        else:
            msg = f'malformed select prefix for the field: {fld}'
            raise ValueError(msg)
        return value

    def title(self, fld):  # pylint: disable=no-self-use
        '''
        sets the title for the data set, going to hard code this as
        test_data
        '''
        LOGGER.debug(f"{fld.field_name}: {data_config.DataSetValues.title}")
        return data_config.DataSetValues.title

    def dataset_slug(self, fld):  # pylint: disable=no-self-use
        '''
        This is currently configured for the name of the dataset to just returning
        the name of the dataset.
        '''
        LOGGER.debug(f"{fld.field_name}: {testConfig.TEST_PACKAGE}")
        return testConfig.TEST_PACKAGE

    def dataset_organization(self, fld):  # pylint: disable=no-self-use
        '''
        :returns: retrieves the name of the organization that is going to be
                 used by the testing and returns it
        '''
        LOGGER.debug(f"{fld.field_name}: {testConfig.TEST_ORGANIZATION}")
        return testConfig.TEST_ORGANIZATION

    def string(self, fld):
        '''
        :return: a random string for the field
        '''
        word = self.rand.getword()
        LOGGER.debug(f"random word assigned to the field {fld.field_name}: {word}")
        return word

    def tag_string_autocomplete(self, fld):
        '''
        Not sure if this should be referencing existing tags... for now
        just making it random text.
        '''
        return self.string(fld)

    def composite_repeating(self, fld, flds2gen=None):  # pylint: disable=no-self-use
        '''
        This type of field is a list made up of a bunch of subfields, this
        call will make a couple calls to this Datapopulation class to generate
        new subfields
        '''
        subfields_values = []
        if flds2gen is None:
            flds2gen = random.randint(1, 3)

        # configured to generate randomly between 1 and 3 subfields the actual
        # range is never actually, just an easy way to create a loop
        for iterval in range(0, flds2gen):  # pylint: unused-variable
            LOGGER.debug(f"flds2gen type: {type(fld.subfields)}")
            population = DataPopulationResource(fld.subfields)
            subfield_data = population.populate_all()
            subfields_values.append(subfield_data)
        return subfields_values

    def multiple_checkbox(self, fld):
        '''
        can select multiple values from the choices.
        '''
        return self.select(fld)

    def date(self, fld):  # pylint: disable=unused-argument
        '''
        :return: a random date.  will be some time between now and 10 years
                 ago.
        '''
        date_1 = datetime.datetime.now()
        delta = datetime.timedelta(days=365 * 10)
        date_2 = date_1 - delta
        rand_date = self.random_date(date_2, date_1)
        return rand_date.strftime('%Y-%m-%d')

    def random_date(self, start, end):
        '''
        Generates a random date string in between the start and end dates
        :param start: the start datetime
        :param end: the end datetime
        :return: a randomly selected date some time in between the two dates.
        '''
        delta = end - start
        LOGGER.debug(f"delta: {delta}")
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        LOGGER.debug(f"int_delta: {int_delta}")
        random_second = random.randrange(int_delta)
        LOGGER.debug(f"random_second: {random_second}")
        return start + datetime.timedelta(seconds=random_second)

    def resource_url_upload(self, fld):
        '''
        :return: gets a random string and then assembles into a url by appending
            https:// and .com
        '''
        randomString = self.string(fld)
        url = f'https://{randomString}.com'
        return url

    def json_object(self, fld):  # pylint: disable=no-self-use, unused-argument
        '''
        right now returning a static json text
        '''
        dummyjson = '{"schema": { "fields":[ { "mode": "nullable", "name": ' + \
                    '"placeName", "type": "string"  },  { "mode": "nullable' + \
                    '", "name": "kind", "type": "string"  }  ] }'
        return dummyjson

    def composite(self, fld):
        '''
        :return: right now just treating the same as composite_repeating but specify
        to only return a single subfield
        '''
        return self.composite_repeating(fld, 1)

    def autocomplete(self, fld):
        '''
        example of what an autocomplete json snippet looks like:
        {
          "field_name": "iso_topic_string",
          "label": "ISO Topic Category",
          "preset": "autocomplete",
          "conditional_field": "bcdc_type",
          "conditional_values": ["geographic"],
          "validators": "conditional_required scheming_multiple_choice",
          "choices": [
            {
              "value": "farming",
              "label": "Farming"
            },
            {
              "value": "biota",
              "label": "Biota"
            },
            {
              "value": "boundaries",
              "label": "Boundaries"
              ...

        Interpretation: if bcdc_type = 'geographic' then fill out this field otherwise
                        don't populate.  verfied with John.

        Method will see if bcdc_type has already been populated, if it has then it
        will process otherwise the processing of this record gets deferred, and is
        tried again after all other records have been processed.

        :return:
        '''
        return self.select(fld)


class UndefinedPreset(AttributeError):
    '''
    Error for when a preset is encountered that has not been coded for.
    '''

    def __init__(self, message, errors=None):  # pylint: disable=unused-argument

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


if __name__ == '__main__':
    # dev work... eventually will have data come from the api end point
    # read data from canned example of data_schema
    dataSchemaFile = os.path.join(os.path.dirname(__file__), '..', 'test_data',
                                  'data_schema.json')
    fh = open(dataSchemaFile, 'r')
    schematext = fh.read()
    fh.close()
    data_struct = json.loads(schematext)

    # simple logging setup
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    hndlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -' +
                                  ' %(lineno)d - %(message)s')
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)
    LOGGER.debug("test")

    # get the possible preset values
    # # presets for datasets
    bcdc_dataset = BCDCDataset(data_struct['dataset_fields'])
    presets = bcdc_dataset.get_presets()
    # # presets for resources
    resources = BCDCDataset(data_struct['resource_fields'])
    resource_preset = resources.get_presets()
    presets.extend(resource_preset)  # combine presets
    presets = list(set(presets))
    presets.sort()
    LOGGER.debug(f'presets: {presets}')
    # TODO: should add methods to validate the returned schema.  Testing is expecting a subset of presets, should make sure that the presets in the data match what is expected if not then throw a useful error message.

    # retrieve the required fields
    bcdc_dataset.set_field_type_filter('required', True)
    for bcdc_dataset_fld in bcdc_dataset:
        fld_nm = bcdc_dataset_fld.get_value('field_name')
        LOGGER.debug(f"field_name: {fld_nm}, {bcdc_dataset_fld.preset}")

    dataset_populator = DataPopulationResource(bcdc_dataset)
    bcdc_dataet = dataset_populator.populate_all()

    resource_populator = DataPopulationResource(resources)
    resources_data = resource_populator.populate_all()

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(bcdc_dataet)

    print('*' * 80)

    pp.pprint(resources_data)

