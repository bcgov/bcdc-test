# Optional Secrets Retrieval

Currently the secret retrieval is set up to retrieve first from environment 
variables.  If those are not found it bounces to searching the secrets file.

Reason is it saves time, not having to define env vars for various runs during 
development.

Secrets file retrieval uses this module: 
https://github.com/bcgov/dbc-pylib/tree/master/DBCSecrets

Docs on how to use it are here: 
https://github.com/bcgov/dbc-pylib/blob/master/docs/secrets.md

# Installing:

### Activte your virtualenv

<path to ve>/scripts

First activate your dev virtualenv, then

*Suspect that on non windows platforms you may not have to include the double*
*around the git module reference.*

`pip install -e "git+https://github.com/bcgov/dbc-pylib@v3.0.7#egg=DBCSecrets&subdirectory=DBCSecrets"`

Once installed create a secrets file with the following content in a secrets
sub directory:

{"pmphost":"",
 "pmprestapidir":"/restapi/json/v1/",
 "pmptoken" : "<don't need now>",
 "miscParams":{
       "__comment__": "just an example don't use for fme parameters", 
       "DLV_HOST": "dev url goes here", 
       "DLV_TOKEN": "api key goes here",
       "TST_HOST": "test url goes here", 
       "TST_TOKEN": "api key for test here", 
       "PRD_HOST": "I think you get the picture", 
       "PRD_TOKEN": ""
  }
}

After this is complete you should be able to proceed with development using the
secrets file.




