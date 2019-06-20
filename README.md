# Automated BCDC API Testing

Intention is to test the CKAN API after deployment.

Current tests include:
 - verification of preconfigured orgs required for testing
 - CRUD tests for packages.

# Run Tests

```
pip install bcdc_apitests
pytest --pyargs bcdc_apitests --junitxml=<xml report name.xml>
```

# Packaging

[packaging docs](docs/packaging.md)

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



