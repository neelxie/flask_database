import psycopg2
import psycopg2.extras
from pprint import pprint
import os

class DatabaseConnection:
    def __init__(self):
        # if os.getenv('DB_NAME') == 'test_flask':
        #     self.db_name = 'test_flask'
        # else:
        #     self.db_name = 'flask_api'
        
        try:
            self.connection = psycopg2.connect(
                dbname='flask_api', user='postgres', host='localhost', password='', port=5432
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            print('Connected to the database successfully')
            # print(self.db_name)
        except:
            pprint("Failed to connect to database.")

    def create_db_tables(self):
        create_table = "CREATE TABLE IF NOT EXISTS users \
            ( first_name VARCHAR(50) NOT NULL, \
            last_name VARCHAR(50) NOT NULL, \
            other_name VARCHAR(50), \
            phone_number VARCHAR(50) NOT NULL, \
            email VARCHAR(50), \
            user_name VARCHAR(50), \
            password VARCHAR(50), \
            is_admin BOOLEAN NOT NULL, \
            user_id SERIAL UNIQUE PRIMARY KEY, \
            registered VARCHAR(50) NOT NULL);"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS Incidents \
            (incident_id SERIAL UNIQUE PRIMARY KEY, \
            created_on VARCHAR(50) NOT NULL, \
            created_by integer REFERENCES Users (user_id) NOT NULL, \
            record_type VARCHAR(10) NOT NULL, \
            incident_comment VARCHAR(200) NOT NULL, \
            location INTEGER NOT NULL, \
            image VARCHAR(50), \
            video VARCHAR(50), \
            status VARCHAR(30));"
        self.cursor.execute(create_table)

    def add_user(self, first_name, last_name, other_name,phone_number, email, username, password,is_admin, user_id, registered):
        query = f"INSERT INTO users ( first_name, last_name, other_name, phone_number, email, username, password, is_admin, user_id, registered) VALUES ('{first_name}', '{last_name}', '{other_name}', '{phone_number}', '{email}', '{username}', '{password}', '{is_admin}', '{user_id}', '{registered}');"
        self.cursor.execute(query)


    def add_incident(self, incident_id, created_on, created_by, record_type, incident_comment, location, image, video, status):
        query = f"INSERT INTO incidents (incident_id, created_on, created_by, record_type, incident_comment, location, image, video, status) VALUES ('{incident_id}', '{created_by}', '{record_type}', '{incident_comment}', '{location}', '{image}', '{video}', '{status}');"
        self.cursor.execute(query)

    


    def get_incidents(self):
        query = "SELECT * FROM incidents;"
        self.cursor.execute(query)
        redflags = self.cursor.fetchall()
        return redflags


    def get_users(self):
        query = "SELECT * FROM users;"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        return users


    def get_an_incident(self, incident_id):
        query = "SELECT * FROM incidents WHERE incident_id= '{incident_id}';"
        self.cursor.execute(query)
        red_flag = self.cursor.fetchone()
        return red_flag


    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE user_id='{user_id}';"
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def check_username(self, username):
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user
    
    def check_email(self, email):
        query = f"SELECT * FROM users WHERE email='{email}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def login(self, username):
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        pprint(user)
        return user


    def update_status(self, status):
        query = "UPDATE incidents SET status = '{status}' WHERE incident_id = '{incident_id}';"
        self.cursor.execute(query)


    def drop_tables(self):
        query = "DROP TABLE users;DROP TABLE incidents; "
        self.cursor.execute(query)
        return "dropped"

if __name__ == '__main__':
    db = DatabaseConnection()