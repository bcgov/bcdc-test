# Automated BCDC API Testing 

Intention is to test the CKAN API after deployment.

Current tests include:
 - verification of preconfigured orgs required for testing
 - CRUD tests for packages.
 
# OC Build

how to create new build without starting
  
```
oc create -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/bcdc-test-buildconfig.yaml
```

start build after created or start future incremental builds.

```
oc start-build bcdc-test
```

# OC Job 

each environment will have its own defined .yaml file within the k8s dir. 

* test-dwelf-job-template.yaml
* test-toyger-job-template.yaml
* test-puma-job-template.yaml

how to run job from yaml as template, so we can change the name using a Generated value appended to name
```
oc process -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/test-dwelf-job-template.yaml | oc create -f -
```


# Run Tests locally

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



