#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper

api = TheHiveApi('http://127.0.0.1:9000', 'IxNbHu15R1G/qOwjcl9i1PV00BID/XSI')
artifacts = []

def makealert(input_title):
    # Prepare the sample Alert
    sourceRef = str(uuid.uuid4())[0:6]
    alert = Alert(title=input_title,
                  tlp=3,
                  tags=['TheHive4Py'],
                  description='N/A',
                  type='external',
                  source='instance1',
                  sourceRef=sourceRef)
    
    # Create the Alert
    response = api.create_alert(alert)
    print(response.text)
    print(response.status_code)

print('Create Alert - should NOT be changed')
makealert("Testing walkoff title")
print('Create Alert - should be changed')
makealert("Testing walkoff portscan title")
print('Create Alert - should NOT be changed')
makealert("Testing walkoff title")
