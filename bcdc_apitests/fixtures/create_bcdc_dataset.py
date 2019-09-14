'''
Created on Sept 13, 2019

@author: KJNETHER

uses the data from scheming end point to construct datasets

'''
import logging
import json



class BCDCSchema(object):
    
    def __init__(self, schema_text):
        self.logger = logging.getLogger(__name__)
        self.schema = json.loads(schema_text)
        self.required_flds = []
        self.optional_flds = []
        
        self.__parse_flds()
        
    def __parse_flds(self):
        '''
        dumps fields into two lists one for required the other optional
        '''
        self.required_flds = []
        self.optional_flds = []
        for fld in self.schema['dataset_fields']:
            if fld['required'] == True:
                self.required_flds.append(fld)
            else:
                self.optional_flds.append(fld)
                
    def get_dataset_required_fields(self):
        
        
        
if __name__ == '__main__':
    # dev work... eventually will have data come from the api end point
    dataSchemaFile = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'data_schema.json')
    fh = open(dataSchemaFile, 'r')
    schematext = fh.read(fh)
    fh.close()
    
    BCDCSchema(dataSchemaFile)