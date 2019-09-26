'''
Created on Sep. 25, 2019

@author: KJNETHER

This module uses mostly the bcdc_dataset_schema module as an interface to the
scheming rules provided via the bcdc scheming extension.

This module will use the scheming data to return actual data that will be used
in the testing.
'''
import datetime
import logging
import random

import randomwordgenerator.randomwordgenerator

import bcdc_apitests.config.testConfig as testConfig
import bcdc_apitests.helpers.data_config as data_config

LOGGER = logging.getLogger(__name__)
WORDS = []


class DataPopulation():
    '''
    This class will subclass the resources population with specific methods
    that return different kinds of test data.
    
    Some examples of what might be returned include iterable classes, 
    like for testing required fi
    '''
    
    def __init__(self, fields_schema):
        self.pop_resource = DataPopulationResource(fields_schema)
        self.fields_schema = fields_schema
        
    def populate_random(self):
        '''
        Returns a single dataset, fields are all randomly populated
        '''
        return self.pop_resource.populate_all()


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

        * if conditional_field exists, then determine the value and populate_random
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
                        don't populate_random.  verfied with John.

        Method will see if bcdc_type has already been populated, if it has then it
        will process otherwise the processing of this record gets deferred, and is
        tried again after all other records have been processed.

        :return:
        '''
        return self.select(fld)

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

        This method will populate_random all the fields defined in the schema, except
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

        LOGGER.debug('populate_random all called')
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
                        # satisfied, don't populate_random, and remove from deferred list
                        if defer_fld.field_name in self.datastruct:
                            del self.datastruct[defer_fld.field_name]
                        to_remove.append(defer_fld)
            # after iteration remove the deferred fields, then try again
            for remove_rec in to_remove:
                self.deferred.remove(remove_rec)
            self.process_deferred_fields()


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


class UndefinedPreset(AttributeError):
    '''
    Error for when a preset is encountered that has not been coded for.
    '''

    def __init__(self, message, errors=None):  # pylint: disable=unused-argument

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


if __name__ == '__main__':
    import os.path
    import json
    import bcdc_apitests.helpers.bcdc_dataset_schema as bcdc_dataset_schema

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

    # BCDC_Dataset Dataset Fields.
    bcdc_dataset = bcdc_dataset_schema.BCDCDataset(dataset_type='dataset_fields',
                               struct=data_struct['result'])

    # # BCDC_Dataset  Resources Fields
    resources = bcdc_dataset_schema.BCDCDataset(dataset_type='resource_fields',
                            struct=data_struct['result'])

    # summarize presets
    presets = bcdc_dataset.get_presets()
    resource_preset = resources.get_presets()
    presets.extend(resource_preset)  # combine presets
    presets = list(set(presets))
    presets.sort()
    LOGGER.debug(f'presets: {presets}')

    # set up a filtered list, Filters at the moment remain untested
    # bcdc_dataset.set_field_type_filter('required', True)
    # for bcdc_dataset_fld in bcdc_dataset:
    #    fld_nm = bcdc_dataset_fld.get_value('field_name')
    #    LOGGER.debug(f"field_name: {fld_nm}, {bcdc_dataset_fld.preset}")

    dataset_populator = DataPopulation(bcdc_dataset)
    bcdc_dataet = dataset_populator.populate_random()

    resource_populator = DataPopulation(resources)
    resources_data = resource_populator.populate_random()

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(bcdc_dataet)

    print('*' * 80)

    pp.pprint(resources_data)
