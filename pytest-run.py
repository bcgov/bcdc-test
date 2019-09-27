import os
import pytest
import sys
import json
from matterhook import Webhook

md_report_path = "/tmp/md-report.md"
xml_report_path = "/tmp/xml-report.xml"
json_report_path = "/tmp/json-report.json"
find_str = "[pytest-md]: https://github.com/hackebrot/pytest-md"
bcdc_url = str(os.getenv('BCDC_URL'))
mat_api_key = str(os.getenv('MATT_API_KEY'))
mat_url = 'https://chat-m.pathfinder.gov.bc.ca'
mat_channel = 'build-and-deploy'
mat_username = 'BCDC-Test'


# ---------- Start Process ------------

#TODO: try catch here
print("Run pytest")
# run pytest cmd
pytest.main(['-v', '--tb=line', '--pyargs', 'bcdc_apitests', '--md', md_report_path,
             ('--junitxml={0}'.format(xml_report_path)), ('--json={0}'.format(json_report_path))])

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
print(tests)
for test in tests:
    result = test['name'] + test['outcome']
    print(result)

# check summary for errors or failed, then set if pass/fail to use later.
# currently set to Fail if any errors or failed.
summary = json_report['report']['summary']
print(summary)
if 'error' or 'failed' in summary:
    print('Failed')
    pass_all = False
else:
    print('Passed')
    pass_all = True

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

# ------------Send Output to Mattermost-------------

# get message to send
mat_message = contents

# mandatory parameters are url and your webhook API key
mwh = Webhook(mat_url, mat_api_key)

# personalized bot name
mwh.username = mat_username

#TODO: try catch here
print("Sending output")
# send a message to the specified channel
mwh.send(mat_message, channel=mat_channel)

print("DONE")

sys.exit(0)


