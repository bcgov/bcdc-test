#!/usr/bin/env python
import os
import pytest
import sys
import json
import requests
from matterhook import Webhook

md_report_path = "/tmp/md-report.md"
xml_report_path = "/tmp/xml-report.xml"
json_report_path = "/tmp/json-report.json"
find_str = "[pytest-md]: https://github.com/hackebrot/pytest-md"
bcdc_url = str(os.getenv('BCDC_URL'))
mat_api_key = str(os.getenv('MATT_API_KEY'))
mat_channel = str(os.getenv('MATT_CHANNEL'))
mat_username = str(os.getenv('MATT_USERNAME'))
mat_url = str(os.getenv('MATT_URL'))
bot_url = str(os.getenv('BOT_URL'))
bot_key = str(os.getenv('BOT_KEY'))
deploy_uid = str(os.getenv('DEPLOY_UID'))

# ---------- Start Process ------------

try:
    # run pytest cmd
    pytest.main(['--tb=line', '--pyargs', 'bcdc_apitests', '--md', md_report_path,
                 ('--junitxml={0}'.format(xml_report_path)), ('--json={0}'.format(json_report_path))])
    print("Running pytest")
    # ---------- Check XML Output ----------

    print("Check xml output")
    print(open(xml_report_path).read())

    # ---------- Check JSON Output ----------

    print("Check json output")
    with open(json_report_path, 'r') as f:
        json_report = json.load(f)
    print(json.dumps(json_report, indent=4, sort_keys=True))

    # testing other outputs
    # playing around with creating custom outputs. testing for now.
    tests = json_report['report']['tests']
    custom_results = []
    print(tests)
    for test in tests:
        result = test['name'] + test['outcome']
        custom_results.append(result)
        print(result)

    # ---------- Pass/Fail Logic ----------------

    # check summary for errors or failed, then set if pass/fail to use later.
    # currently set to Fail if any errors or failed.
    summary = json_report['report']['summary']
    print(summary)

    if any(k in summary for k in ("error", "failed")):
        print("Failed as found either error or failed values")
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

    # ---------- Update Markdown File ----------------

    print("update markdown output")
    # cleanup markdown output
    with open(md_report_path, "r") as f:
        modified_output = []
        lines = f.readlines()
        if pass_all:
            lines[0] = "## Passed\n"
        else:
            lines[0] = "## Failed\n"

        for line in lines:
            modified_output.append(line.replace(find_str, bcdc_url))

    # add custom_results to end of md output
    for result in custom_results:
        modified_output.extend(result + '\n')

    print("write to markdown file")
    # re-write file.
    with open(md_report_path, "w") as f:
        for line in modified_output:
            f.writelines(line)

    print("Get markdown file to send to mattermost")
    # read file and store
    inFile = open(md_report_path, 'r')
    contents = inFile.read()
    print(contents)

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
    mat_message = contents

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




