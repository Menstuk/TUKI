from colorama import Fore, Style
import mysql.connector

class DB_connect:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password123'
        self.db_name = None

    def connect_db(self):
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Connecting to Data Base>")
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password
            )
        return mydb
    
    def create_database(self, cursor):
        cursor.execute("CREATE DATABASE IF NOT EXISTS EnglishTeacher")
        cursor.execute("USE EnglishTeacher")
    
    def create_users_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(256) NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        """)