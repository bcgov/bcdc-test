# Automated BCDC API Testing 

Intention is to test the CKAN API after deployment.

Current tests include:
 - verification of preconfigured orgs required for testing
 - CRUD tests for packages.
 
# OC Build for BCDC-TEST

pulls package from https://pypi.org/project/bcdc-apitests/
new OC build triggered by github actions on commit to master branch

how to create new build from build config
  
```
oc create -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/bcdc-test-buildconfig.yaml
```

start build 

```
oc start-build bcdc-test -n databcdc
```

# OC Jobs for BCDC-TEST

each environment will have its own defined .yaml file within the k8s dir. 

* test-dwelf-job-template.yaml
* test-toyger-job-template.yaml

how to run job from yaml as template, so we can change the name using a generated value appended to name
* CADI
```
oc process -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/test-dwelf-job-template.yaml | oc create -f -
```
* CATI
```
oc process -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/test-toyger-job-template.yaml | oc create -f -
```


# OC Development Build for BCDC-TEST-DEV

pulls from https://pypi.org/project/bcdc-apitests-dev/
new OC build triggered by github actions on push to dev branch

```
oc create -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/bcdc-test-buildconfig-dev.yaml
```

# OC Developmnet Jobs for BCDC-TEST-DEV
* CADI
```
oc process -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/test-dwelf-job-template-dev.yaml | oc create -f -
```
* CATI
```
oc process -f https://raw.githubusercontent.com/bcgov/bcdc-test/dev/k8s/test-toyger-job-template-dev.yaml | oc create -f -
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



