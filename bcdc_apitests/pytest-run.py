#!/usr/bin/env python
import os
import pytest
import sys
import json
import requests
from matterhook import Webhook

# output paths
xml_report_path = "/tmp/xml-report.xml"
json_report_path = "/tmp/json-report.json"

# env vars
bcdc_url = str(os.getenv('BCDC_URL'))
mat_api_key = str(os.getenv('MATT_API_KEY'))
mat_channel = str(os.getenv('MATT_CHANNEL'))
mat_username = str(os.getenv('MATT_USERNAME'))
mat_url = str(os.getenv('MATT_URL'))
bot_url = str(os.getenv('BOT_URL'))
bot_key = str(os.getenv('BOT_KEY'))
deploy_uid = str(os.getenv('DEPLOY_UID'))

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

    # ---------- Pass/Fail Logic ----------------

    # check summary for failed, then set if pass/fail to use later.
    # currently set to Fail if any errors or failed.
    summary = json_report['report']['summary']
    print(summary)

    if any(k in summary for k in ("failed")):
        print("Failed as found either failed values")
        pass_all = False
        status = 'Failed'
    elif "passed" in summary:
        print("Passed with no Error or Failed Values")
        pass_all = True
        status = 'Passed'
    else:
        print("Failed to find a Passed Value")
        pass_all = False
        status = 'Failed'

    # ---------- create markdown output to send ---------------

    markdown = 'BCDC API Test Results' + '\n'
    markdown += status + ' ' + bcdc_url + '\n'
    markdown += str(summary) + '\n'
    markdown += '\n'
    for result in custom_results:
        to_add = result + '\n'
        markdown += to_add
    markdown += "\n"

    print(markdown)

    # ------------Send Output to Hubot ------------------
    # TODO: try catch and update payload to be full test json output.
    print("Sending Output to Hubot")
    botPath = bot_url+'/hubot/apitest'
    print(botPath)
    response = requests.post(
        botPath,
        headers={'Content-Type': 'application/json', 'apikey': bot_key},
        json={"status": status, "env": bcdc_url, "results": summary, "id": deploy_uid}
    )
    print(response)

    # ------------Send Output to Mattermost-------------

    # get message to send
    mat_message = markdown

    # mandatory parameters are url and your webhook API key
    mwh = Webhook(mat_url, mat_api_key)

    # personalized bot name
    mwh.username = mat_username

    try:
        # send a message to the specified channel
        mwh.send(mat_message, channel=mat_channel)
        print("Sending output to mattermost")
    except Exception as e:
        print(e)

    print("script completed")
    sys.exit(0)

except Exception as e:
    print(e)
    sys.exit(1)




