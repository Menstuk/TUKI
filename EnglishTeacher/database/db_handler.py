from colorama import Fore, Style
import mysql.connector

class DB_connect:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password123'
        self.db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password
            )
        self.cursor = self.db.cursor()

    # def connect_db(self):
    #     '''
    #     Starting the data base connection
    #     print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connecting to Data Base>")
    #     '''
    #     mydb = mysql.connector.connect(
    #         host = self.host,
    #         user = self.user,
    #         passwd = self.password
    #         )
    #     self.db = mydb
    #     print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connected Succesfully to DB>")
    #     return mydb
    
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
                username VARCHAR(256) PRIMARY KEY,
                password VARCHAR(50) NOT NULL,
                level VARCHAR(8) DEFAULT 'low'
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
                speech_rate_score FLOAT,
                questions_score FLOAT,
                grammar_score FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (username, timestamp),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
    
    def drop_database(self, cursor, database_name):
        # Drop the existing database
        cursor.execute("DROP DATABASE IF EXISTS {}".format(database_name))

        # Commit changes
        self.db.commit()


    def create_all_tables(self, cursor):
        self.create_users_table(cursor)
        self.create_user_metrics_table(cursor)

    def insert_user_stats(self, cursor, username, speech_rate, speech_rate_score, questions_score, grammar_score):
        '''
        Insert new record of user test with 4 metrics: speech_rate, speech_rate_score, questions_score
        and grammar_score.
        Will be called after the user will finish a test and the metrics will be calculated 
        '''
        print(f"You speak at a rate of: {speech_rate} words per second")
        print(f"Your speech rate score is: {speech_rate_score} / 5")
        print(f"Your answered questions grade is: {questions_score} / 5")
        print(f"Your grammar score is: {grammar_score} / 5")
        insert_query = "INSERT INTO user_metrics (username, speech_rate, speech_rate_score, \
            questions_score, grammar_score) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (username, speech_rate, speech_rate_score, questions_score, grammar_score))
        self.db.commit()
        update_query = """
            UPDATE users
            SET level = %s
            WHERE username = %s
        """
        level = "low"
        if speech_rate_score >= 4 and questions_score == 5 and grammar_score >= 4:
            level = "high"
        elif speech_rate_score >= 2 and questions_score >= 3 and grammar_score >= 3:
            level = "medium"
        cursor.execute(update_query, (level, username))
        self.db.commit()
        print(f"Your English level is: {level}")
        print("User stats inserted successfully!")