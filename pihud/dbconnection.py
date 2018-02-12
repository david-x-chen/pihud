
import psycopg2

class DbConnection():
    def connect():
        	conn_string = "host='localhost' dbname='my_database' user='postgres' password='secret'"
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            return cursor

    def saveData(cursor, infotype, stringvalue, numericvalue, actualvalue):
        query = """
        INSERT INTO public.obd2info(trackdate, infotype, stringvalue, numericvalue, actualvalue)
        VALUES (NOW(), %s, %s, %s, %s)
        """
        values = (infotype, stringvalue, numericvalue, actualvalue)
        cursor.execute(query, values)
