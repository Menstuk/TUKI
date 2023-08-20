from colorama import Fore, Style
import mysql.connector

class DB_connect:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password123'
        self.db = None

    def connect_db(self):
        '''
        Starting the data base connection
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connecting to Data Base>")
        '''
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password
            )
        self.db = mydb
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connected Succesfully to DB>")
        return mydb
    
    def create_database(self, cursor):
        '''
        Create data base if not exist yet
        '''
        cursor.execute("CREATE DATABASE IF NOT EXISTS EnglishTeacher")
        cursor.execute("USE EnglishTeacher")
    
    def create_users_table(self, cursor):
        '''
        Create general user table for sign up\in and identify users
        '''
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(256) NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        """)
    
    def create_user_metrics_table(self, cursor):
        '''
        Create the table that will store user data and progress using timestamp to track improvement over time
        '''
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_metrics (
                username VARCHAR(256),
                speech_rate FLOAT,
                correct_answers_metric FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (username, timestamp),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
    
    def insert_user_metrics(self, cursor, username, speech_rate, correct_answers_metric):
        '''
        Insert new record of user test with the 2 metrics: speech_rate, correct_answers_metric 
        Will be called after the user will finish a test and the metrics will be calculated 
        '''
        insert_query = "INSERT INTO user_metrics (username, speech_rate, correct_answers_metric) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, speech_rate, correct_answers_metric))
        self.db.commit()
        # print("User metrics inserted successfully!")