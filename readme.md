# Automated BCDC API Testing

Intention is to test the CKAN API after deployment.

Current tests include:
 - verification of preconfigured orgs required for testing
 - CRUD tests for packages.
 
# Running Tests

### clone
`git clone <repo>`

### virtualenv 
```
python -m virtualenv ve_bcdctest
./ve_bcdctest/Scripts/activate
python -m pip install -r requirements.txt
```

* make SRC dir part of python path
```
export PYTHONPATH=./src
set PYTHONPATH=./src
```

### configure secrets
set the following env vars:

```
BCDC_API_KEY = <api key>
BCDC_URL = <URL>
```

### run tests
```
cd src
pytest
```

# Running Tests using Docker

### Environment Variables

Somehow you need to have these two environment variables available to the tests
when they are run:

* BCDC_API_KEY
* BCDC_URL

Easiest way is to create a docker environment file which will look like:

```
BCDC_API_KEY = <api key>
BCDC_URL = <URL>
```

### Building
`docker build --tag=bcdc_test .`

### Running
`docker run --env-file={env file} bcdc_test`



