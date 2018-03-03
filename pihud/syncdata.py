#!/usr/bin/python3
import psycopg2
import sys
import json
import requests
import os
from GlobalConfig import GlobalConfig

# file paths
running_dir         = os.path.dirname(os.path.realpath(__file__))
default_config_path = os.path.join(running_dir, 'default.rc')
config_path         = os.path.join(os.path.expanduser('~'), 'pihud.rc')

class SyncData():
    def __init__(self):
        if not os.path.isfile(config_path):
            # copy the default config
            if not os.path.isfile(default_config_path):
                print("[pihud] Fatal: Missing default config file. Try reinstalling")
                sys.exit(1)
            else:
                shutil.copyfile(default_config_path, config_path)

        global_config = GlobalConfig(config_path)

        conn_string = global_config["conn_string"]

        self.connection = None
        self.cursor = None
        self.obdata = []

        self.requiredInfoTypes = [
    		"RPM", "SPEED", "STATUS", "ENGINE_LOAD", "SHORT_FUEL_TRIM_1", "LONG_FUEL_TRIM_1",
    		"THROTTLE_POS", "COMMANDED_EQUIV_RATIO", "MAF", "INTAKE_TEMP", "COOLANT_TEMP",
    		"CONTROL_MODULE_VOLTAGE", "TIMING_ADVANCE", "RUN_TIME"]

        if self.connection is None:
            self.connection = psycopg2.connect(conn_string)

    def startingDateUnix(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT EXTRACT(EPOCH FROM min(trackdate)::TIMESTAMP WITH TIME ZONE) FROM public.obd2info")
        row = cursor.fetchone()

        return float(row[0])

    def retrieveData(self, infotype, trackdateUnix):
        cursor = self.connection.cursor()
        cursor.execute("select EXTRACT(EPOCH FROM trackdate::TIMESTAMP WITH TIME ZONE), trackdate, infotype, stringvalue, numericvalue, actualvalue from obd2info where infotype='%s' AND trackdate >= to_timestamp(%d) limit 10", (infotype, trackdateUnix))
        print("Row number:", cursor.rowcount)
        row = cursor.fetchone()
        while row is not None:
            self.obdata.append(OBD2Data(row[0], row[1], row[2], row[3], row[4], row[5]))
            row = cursor.fetchone()
        cursor.close()
        return self.obdata

    def toJson(self, infotype, trackdateUnix):
        syncedData = self.retrieveData(infotype, trackdateUnix)
        return json.dumps(syncedData.__dict__)

    def postData(self):
        trackdateUnix = self.startingDateUnix();
        for t in self.requiredInfoTypes:
            jsonStr = self.toJson(t, trackdateUnix)

            url = "https://dyntechsolution.info/car/cartracker/" + t
            print(url)
            data = jsonStr

            headers = {'Content-type': 'application/json'}

            r = requests.post(url, headers=headers, json=data)

        for d in self.obdata:
            print(d.trackdateUnix)
            cursor = self.connection.cursor()
            self.connection.deleteData(d.infotype, d.trackdateUnix)

        return 200

class OBD2Data:
    def __init__(self,
                 trackdateUnix = None,
                 trackdate     = None,
                 infotype      = None,
                 stringvalue   = None,
                 numericvalue  = None,
                 actualvalue   = None):

        self.trackdateUnix = trackdateUnix
        self.trackdate     = trackdate
        self.infotype      = infortype
        self.stringvalue   = stringvalue
        self.numericvalue  = numericvalue
        self.actualvalue   = actualvalue

def main():
    db = SyncData()
    status = db.postData()
    print(status)
    if db.connection is not None:
        db.connection.close()

if __name__ == "__main__":
    main()
