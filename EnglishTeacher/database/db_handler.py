import json

import pathlib
from colorama import Fore, Style
import mysql.connector

with open(pathlib.Path().absolute().parent / "configuration.json", "r") as f:
    cfg = json.load(f)

db_params = cfg["db_handler"]


class DB_connect:
    def __init__(self):
        self.host = db_params["init"]["host"]
        self.user = db_params["init"]["user"]
        self.password = db_params["init"]["password"]
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password
            )
        self.cursor = self.db.cursor()

    # def connect_db(self):
    #     '''
    #     Starting the database connection
    #     print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connecting to Data Base>")
    #     '''
    #     mydb = mysql.connector.connect(
    #         host = self.host,
    #         user = self.user,
    #         passwd = self.password
    #         )
    #     self.db = mydb
    #     print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connected Successfully to DB>")
    #     return mydb
    
    def create_database(self, cursor):
        """
        Create database if it doesn't exist yet
        """
        cursor.execute("CREATE DATABASE IF NOT EXISTS EnglishTeacher")
        cursor.execute("USE EnglishTeacher")
    
    def create_users_table(self, cursor):
        """
        Create general user table for sign up\in and identify users
        """
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(256) PRIMARY KEY,
                password VARCHAR(50) NOT NULL,
                level VARCHAR(8) DEFAULT 'low'
            )
        """)
    
    def create_user_metrics_table(self, cursor):
        """
        Create the table that will store user data and progress using timestamp to track improvement over time
        """
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
        """
        Insert new record of user test with 4 metrics: speech_rate, speech_rate_score, questions_score
        and grammar_score.
        Will be called after the user will finish a test and the metrics will be calculated 
        """
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"You speak at a rate of: {speech_rate} words per second")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Your speech rate score is: {speech_rate_score} / 5")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Your answered questions grade is: {questions_score} / 5")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Your grammar score is: {grammar_score} / 5\n")
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
        if ((speech_rate_score >= db_params["user_stats"]["high1"]["speech_rate_score"] and
            questions_score == db_params["user_stats"]["high1"]["questions_score"] and
            grammar_score >= db_params["user_stats"]["high1"]["grammar_score"])
            or
            (speech_rate_score == db_params["user_stats"]["high2"]["speech_rate_score"] and
            questions_score == db_params["user_stats"]["high2"]["questions_score"] and
                grammar_score == db_params["user_stats"]["high2"]["grammar_score"])):
            level = "high"
        elif (speech_rate_score >= db_params["user_stats"]["medium"]["speech_rate_score"] and
              questions_score >= db_params["user_stats"]["medium"]["questions_score"] and
              grammar_score >= db_params["user_stats"]["medium"]["grammar_score"]):
            level = "medium"
        cursor.execute(update_query, (level, username))
        self.db.commit()
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"Your English level is: {level}")
        print(Fore.LIGHTBLUE_EX + Style.DIM + "User stats inserted successfully!\n")
