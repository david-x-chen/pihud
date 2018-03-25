#!/usr/bin/python3
import sys
from json import dumps, loads, JSONEncoder, JSONDecoder
import requests
import os
import time
from collections import namedtuple

class SyncData():
    def __init__(self):

        self.requiredInfoTypes = [
    		"RPM", "SPEED", "STATUS", "ENGINE_LOAD", "SHORT_FUEL_TRIM_1", "LONG_FUEL_TRIM_1",
    		"THROTTLE_POS", "COMMANDED_EQUIV_RATIO", "MAF", "INTAKE_TEMP", "COOLANT_TEMP",
    		"CONTROL_MODULE_VOLTAGE", "TIMING_ADVANCE", "RUN_TIME"]

    def postData(d):
        jsonStr = dumps(d.__dict__)
        print(jsonStr)
        url = "https://dyntechsolution.info/car/cartracker/" + infotype
        print(url)
        data = jsonStr

        headers = {'Content-type': 'application/json'}

        r = requests.post(url, headers=headers, data=jsonStr)
        print(r.content)
        print(r.status_code)

        return 200

OBD2Data = namedtuple('OBD2Data', 'trackdateUnix infotype stringvalue numericvalue actualvalue')
