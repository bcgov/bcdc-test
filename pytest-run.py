import os
import pytest
import sys
from matterhook import Webhook
from tempfile import NamedTemporaryFile

# create tempfile
f = NamedTemporaryFile()
temp_filename = f.name
print(temp_filename)


md_report_path = temp_filename
find_str = "[pytest-md]: https://github.com/hackebrot/pytest-md"
bcdc_url = str(os.getenv('BCDC_URL'))
mat_api_key = str(os.getenv('MATT_API_KEY'))
mat_url = 'https://chat-m.pathfinder.gov.bc.ca'
mat_channel = 'build-and-deploy'
mat_username = 'ckantest'


# ----------Start Process -----------
print("start")
# run pytest cmd
pytest.main(['-v', '--tb=line', '--pyargs', 'bcdc_apitests', '--md', md_report_path])

print("update-output")
# cleanup md output and add our env var
with open(md_report_path, "r") as f:
    modified_output=[]
    for line in f.readlines():
        modified_output.append(line.replace(find_str, bcdc_url))

print("write-file")
# re-write file.
with open(md_report_path, "w") as f:
    for line in modified_output:
        f.writelines(line)

print("get-output")
# read file and store
inFile = open(md_report_path, 'r')
contents = inFile.read()
print(contents)

# ------------Send Output to Mattermost-------------
# mat_message = BCDC_URL + " Test results coming soon to a Mattermost channel near you."
mat_message = contents

# mandatory parameters are url and your webhook API key
mwh = Webhook(mat_url, mat_api_key)

# personalized bot name
mwh.username = mat_username

print("share-output")
# send a message to the specified channel
mwh.send(mat_message, channel=mat_channel)

print("DONE")

sys.exit(0)


