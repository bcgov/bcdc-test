# Packaging

### Create python package:

`python setup.py sdist bdist_wheel`

### Upload to pypi (test)

`python -m twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*`


# Dockerfile testing

```
set TWINE_PASSWORD=<pypi pswd>
set TWINE_USERNAME=<pypi username>
docker build .
```

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
pytest --pyargs bcdc_apitests
```

to create a JUNIT xml report cann run:
`pytest --pyargs bcdc_apitests --junitxml=<path to junit xml report>`

