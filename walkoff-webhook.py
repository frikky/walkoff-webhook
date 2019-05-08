import os
import time
import json
import requests
from flask import Flask, request

url = "http://localhost:8080/api"
status = ""
def get_access_token(headers):
    username = "admin"
    password = "admin"

    fullurl = "%s/auth" % url
    data = {
        "username": username,
        "password": password
    }

    ret = requests.post(fullurl, headers=headers, auth=(username, password), json=data)
    if ret.status_code != 201:
        print("Exiting - bad return")
        exit()

    return ret.json()["access_token"], ret.json()["refresh_token"]

def get_workflows(headers):
    fullurl = "%s/workflows" % url
    ret = requests.get(fullurl, headers=headers)
    if ret.status_code != 200:
        print("Exiting workflows - get")
        exit()

    return ret

def run_workflow(headers, data):
    fullurl = "%s/workflowqueue" % url
    ret = requests.post(fullurl, headers=headers, json=data)

    if ret.status_code != 202:
        print(ret.text)
        print(ret.status_code)
        print("Exiting workflows - run queue")
        exit()

    return ret

def get_workflow_status(headers, execution_id):
    fullurl = "%s/workflowqueue/%s" % (url, execution_id)
    ret = requests.get(fullurl, headers=headers)
    if ret.status_code != 200:
        print(ret.text)
        print(ret.status_code)
        print("Exiting wrokflow status")
        exit()

    return ret

def update_workflow(headers, item):
    fullurl = "%s/workflows" % url
    print(fullurl)

    ret = requests.post(fullurl, headers=headers, json=item)
    if ret.status_code != 201:
        print(ret.text)
        print(ret.status_code)
        print("Exiting wrokflows")
        exit()

    return ret

def verify_complete(headers, workflow_ret):
    # Code used to verify whether it ran or not
    cnt = 0
    sleep = 1
    while(1):
        status = get_workflow_status(headers, workflow_ret.json()["execution_id"])
        if status.json()["status"] == "COMPLETED":
            print("COMPLETE!!")
            break

        if cnt % 10 == 0:
            print(status.json())

        cnt += 1
        time.sleep(sleep)

    print("Used %d seconds to execute" % cnt*sleep)
    status = status.text


def run_walkoff(input_variable, event):
    headers = {"Content-Type": "application/json"}
    access_token, refresh_token = get_access_token(headers)
    headers["Authorization"] = "Bearer %s" % access_token

    # Cache this somehow
    workflows = get_workflows(headers)

    executed = False
    for item in workflows.json():
        # Find the ID correlating first
        if item["name"] != input_variable:
            continue

        # Setting up the data being sent to run a workflow
        data = {
            "workflow_id": item["id_"],
        }

        # Used to only update one
        found = False
        for param in item["workflow_variables"]:
            if param["name"] == "webhook_input":
                data["workflow_variables"] = []
                data["workflow_variables"].append({
                    "id_": param["id_"],
                    "name": param["name"],
                    "value": str(event),
                })

                found = True
                break

        if not found:
            print("Workflow environment variable \"webhook_input\" for %s doesn't exist!! Please create it" % input_variable)
            break

        executed = True
            
        # Remove this del data in the future when the intended way works.
        # Deleting, as this doesn't work yet. WALKOFF code states "TODO" for this same bit. 
        # What it does: Swaps environment variable "webhook_input". 
        # Might make inconsistency issues if you're not careful (message queue could fix this)
        if len(item["workflow_variables"]) == len(data["workflow_variables"]):
            item["workflow_variables"] = data["workflow_variables"]
        # Updates the workflow as the backend should do in the future
        update_workflow(headers, item)
        del data["workflow_variables"]

        # Runs the actual workflow named e.g. AlertUpdate with the
        # environment variable "workflow_variables" set to the webhook input
        workflow_ret = run_workflow(headers, data)

        # Uncomment this to verify whether it completed or not
        # verify_complete(headers, workflow_ret)

    if not executed:
        # Lets make it :)
        print("No execution ready for WALKOFF at %s in %s." % (url, input_variable))
    else:
        print()
        if not status:
            print("Ran without verifying result. Probably ran :)")
        else:
            print("Echo return: %s" % status)
            

# Initialize the app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Allowed events (based on thehive docs)
events = [
    'AlertCreation',
    'AlertUpdate',
    'CaseArtifactCreation',
    'CaseArtifactJobCreation',
    'CaseArtifactJobUpdate',
    'CaseArtifactJobUpdate',
    'CaseArtifactUpdate',
    'CaseCreation',
    'CaseTaskCreation',
    'CaseTaskLogCreation',
    'CaseTaskUpdate',
    'CaseUpdate'
]

def capitalize(event_name):
    event_name = event_name.replace('_', ' ')
    return ''.join(x for x in event_name.title() if not x.isspace())

@app.route('/', methods=['GET'])
def index():
    return 'TheHiveHooks'

@app.route("/webhook", methods=['POST'])
def webhook():
    event = request.get_json()
    event_name = capitalize('{}_{}'.format(event['objectType'], event['operation']))
    print(event_name)
    if event_name in events:
        run_walkoff(event_name, event)

    return json.dumps(event, indent=4, sort_keys=True)

port = int(os.environ.get('PORT', 9091))
app.run(host='0.0.0.0', port=port, debug=True)
