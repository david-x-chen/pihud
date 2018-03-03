
import psycopg2

class DbConnection():
    def connect(conn_string):
        #conn_string = "host='localhost' dbname='cartracker' user='pi' password='password'"
        conn = psycopg2.connect(conn_string)
        return conn

    def saveData(cur, infotype, stringvalue, numericvalue, actualvalue):
        query = """
        INSERT INTO public.obd2info(infotype, stringvalue, numericvalue, actualvalue)
        VALUES (%s, %s, %s, %s)
        """
        values = (infotype, stringvalue, numericvalue, actualvalue)
        cur.execute(query, values)

    def deleteData(cur, infotype, trackDateUnix):
        query = """
        DELETE FROM public.obd2info
        WHERE infotype = '%s' AND trackdate <= to_timestamp(%d)
        """
        values = (infotype, trackDateUnix)
        cur.execute(query, values)
