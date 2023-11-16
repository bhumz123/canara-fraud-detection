import json
import psycopg2


class PostgreClient:

    def __init__(self):
        try:
            # Establish connection to the PostgreSQL database
            self.connection = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='1234',
                database='test_db'
            )
            self.cursor = self.connection.cursor()
            # Connection is successful
            print("Connection to PostgreSQL successful")
            create_table_query = '''
                 CREATE TABLE IF NOT EXISTS demo (
                     timestamp TIMESTAMP,
                     event_key VARCHAR(500),
                     event_data JSONB,
                     status VARCHAR(50),
                     predicted_value VARCHAR(50)
                 );'''

            self.cursor.execute(create_table_query)
            self.connection.commit()

        except (psycopg2.Error, Exception) as error:
            print("Error while connecting to PostgreSQL:", error)

    def send_to_db(self,tm ,key, event):
        try:
            query = '''INSERT INTO demo (timestamp, event_key, event_data, status)
                 VALUES (%s, %s, %s, %s);'''
            status = 'PENDING'
            self.cursor.execute(query, (tm, str(key), json.dumps(event), status))
            self.connection.commit()
            print("Commit to Database Successful")
            return 0
        except (psycopg2.Error, Exception) as e:
            print("Could not send data to db", e)
            return 1
