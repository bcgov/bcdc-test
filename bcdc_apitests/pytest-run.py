#!/usr/bin/env python
import os
import pytest
import sys
import json
import requests


# output paths
xml_report_path = "/tmp/xml-report.xml"
json_report_path = "/tmp/json-report.json"

# required env vars
bcdc_url = str(os.getenv('BCDC_URL'))
jenkins_callback_url = str(os.getenv('JENKINS_CALLBACK_URL'))
jenkins_callback_username = str(os.getenv('JENKINS_CALLBACK_USERNAME'))
jenkins_callback_token = str(os.getenv('JENKINS_CALLBACK_TOKEN'))

# set logging level to INFO if not set

if os.getenv('LOG_LEVEL') is None:
    log_level = "INFO"
    print("log level was NOT set, setting to: " + log_level)
else:
    log_level = str( os.getenv('LOG_LEVEL'))
    print("log level set to: " + log_level)

# ---------- Start Process ------------

try:

    # ---------- start pytest ----------
    # run pytest cmd
    print("Running pytest")
    # pytest with both xml and json output, only using json output at this time.

    pytest.main(['-o', 'log_cli=true', ('--log-cli-level={0}'.format(log_level)), '--pyargs', 'bcdc_apitests',
                 ('--junitxml={0}'.format(xml_report_path)), ('--json={0}'.format(json_report_path))])

    # For Development Work only , to run one module
    # pytest.main(['-o', 'log_cli=true', ('--log-cli-level={0}'.format(log_level)),
    #              '/usr/local/lib/python3.8/site-packages/bcdc_apitests/tests/other',
    #              ('--junitxml={0}'.format(xml_report_path)), ('--json={0}'.format(json_report_path))])


    # ---------- Check JSON Output ----------

    # get json test results
    print("Test Results as json output")
    with open(json_report_path, 'r') as f:
        json_report = json.load(f)
    print(json.dumps(json_report, indent=4, sort_keys=True))

    tests = json_report['report']['tests']
    custom_results = []

    # get test results name and outcome as list
    for test in tests:
        result = test['outcome'] + ' ' + test['name']
        custom_results.append(result)

    print(custom_results)

    # ---------- Pass/Fail Logic ----------------

    # check summary for failed, then set if pass/fail to use later.
    # currently set to Fail if any errors or failed.
    summary = json_report['report']['summary']
    print(summary)

    if any(k in summary for k in ("failed", "null")):
        print("Failed as found either failed values")
        status = 'fail'
    elif "passed" in summary:
        print("Passed with no Error or Failed Values")
        status = 'pass'
    else:
        print("Failed to find a Passed Value")
        status = 'fail'

    # ---------- Send Results ----------------
    # Callback Jenkins CICD with results
    print("Callback Jenkins with results: " + jenkins_callback_url)

    # payload requires status var to be pass or fail
    payload = {
        'json': (None, '{"parameter": {"name": "STATUS", "value": "' + status + '"}}'''),
        'proceed': (None, 'Proceed'),
    }
    response = requests.post(url=jenkins_callback_url, files=payload,
                             auth=(jenkins_callback_username, jenkins_callback_token))


    print("script completed")
    sys.exit(0)

except Exception as e:
    print(e)
    sys.exit(1)




