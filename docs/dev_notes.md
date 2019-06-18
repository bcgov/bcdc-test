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

## Activate your virtualenv

#### Windoze

`<path to ve>/Scripts/activate`

#### Everyone else (mak, linux)
`source <path to ve>/bin/activate`

## Install Secrets Module

`pip install -e "git+https://github.com/bcgov/dbc-pylib@v3.0.7#egg=DBCSecrets&subdirectory=DBCSecrets"`
`pip install -e "git+https://github.com/bcgov/dbc-pylib@v3.0.7#egg=PMP&subdirectory=PMP"`
*Suspect that on non windows platforms you may not have to include the double*
*around the git module reference.*

## Configure Secrets

Once installed create a secrets file with the following content in a secrets
sub directory:

```
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
```

After this is complete you should be able to proceed with development using the
secrets file.

# Future Development strategy.

Thinking the secrets file should use the same names as the expected environment
variables.  Also the tokens should identify the roles that they have... so down 
the road tests expected env vars would change from:

`BCDC_API_KEY=<api token> `

to 

```
BCDC_API_KEY_VIEWER=<api token> 
BCDC_API_KEY_EDITOR=<api token> 
BCDC_API_KEY_ADMIN=<api token> 
BCDC_API_KEY_BRUCEALLMIGHTY=<api token>
```
