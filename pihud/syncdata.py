#!/usr/bin/python3
import psycopg2
import sys

class SyncData():
    def __init__(self):
        conn_string = "host='localhost' dbname='cartracker' user='pi' password='password'"

        self.connection = None
        self.cursor = None
        self.obdata = []

        if self.connection is None:
            self.connection = psycopg2.connect(conn_string)

    def retrieveData(self):
        cursor = self.connection.cursor()
        cursor.execute("select * from obd2info")
        print("Row number:", cursor.rowcount)
        row = cursor.fetchone()
        while row is not None:
            self.obdata.append(OBD2Data(row[0], row[1], row[2], row[3], row[4]))
            row = cursor.fetchone()
        cursor.close()
        return self.obdata

class OBD2Data:
    def __init__(self,
                 trackdate    = None,
                 infotype     = None,
                 stringvalue  = None,
                 numericvalue = None,
                 actualvalue  = None):

        self.trackdate    = trackdate
        self.infotype     = infortype
        self.stringvalue  = stringvalue
        self.numericvalue = numericvalue
        self.actualvalue  = actualvalue

def main():
    db = SyncData()
    syncedData = db.retrieveData()
    print(len(syncedData))
    if db.connection is not None:
        db.connection.close()

if __name__ == "__main__":
    main()
