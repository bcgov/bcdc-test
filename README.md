# Automated BCDC API Testing

Intention is to test the CKAN API after deployment.

Current tests include:
 - verification of preconfigured orgs required for testing
 - CRUD tests for packages.

# Run Tests

```
pip install ckanext-bcdc-apitests
pytest --pyargs ckanext_bcdc_apitests --junitxml=<xml report name.xml>
```

# Packaging

### Create python package:

`python setup.py sdist bdist_wheel`

### Upload to pypi (test)

`python -m twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*`

### Test (test) package
```
mkdir junk
cd junk
python -m virtualenv junk_ve
junk_ve/Scripts/activate
pip install pytest requests ckanapi
pip install --index-url https://test.pypi.org/simple/ --no-deps ckanext_bcdc_apitests --upgrade
set BCDC_API_KEY = <api key>
set BCDC_URL = <URL>
pytest --pyargs ckanext_bcdc_apitests
```

to create a JUNIT xml report cann run:
`pytest --pyargs ckanext_bcdc_apitests --junitxml=<path to junit xml report>`

### Upload to pypi (prod)

`python -m twine upload --verbose dist/*`

Now the package ckanext_bcdc_apitests should install just like any other python
package


# Configure Dev Env and Running Tests

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



