from colorama import Fore, Style

class Signing:
    def __init__(self):
        self.user_name = None
        

    def sign_up(self, db, cursor):
        '''
        Sign up for new user, forcing unique username and taking care of updating users table
        '''
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Sign Up>")
        while True:
            user_name = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Please enter your username: ")
            if self.username_exists(cursor, user_name): # Check if username already exists
                print(Fore.RED + Style.BRIGHT + "Username already taken. Please choose different username.")
            else:
                break
        passwd = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Please enter your password: ")
        
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (user_name, passwd))
        db.commit()
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + user_name + " registered successfully")
        self.user_name = user_name
        return self.user_name
    
    def sign_in(self, db, cursor):
        '''
        Signing in user with username and password, if not succeeded user can try again or exit
        '''
        log_in_flag = False
        while not log_in_flag: 
            print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Sign In>")
            user_name = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Please enter your username: ")
            passwd = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Please enter your password: ")
            
            select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(select_query, (user_name, passwd))
            
            if cursor.fetchone(): # If user identified succesfully
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Hey " + user_name + ", nice to see you again!")
                log_in_flag = True
            else: # If not he can try again or quit
                print(Fore.RED + Style.BRIGHT + "Invalid username or password.")
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "-------------------------------")
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "1. Try Again")
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "2. Exit")
                choice = int(input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Enter your choice: "))
                if choice == 2:
                    break
        if log_in_flag:
            self.user_name = user_name
        return log_in_flag, self.user_name
    
    def username_exists(self, cursor, username):
        '''
        Checks if username is unique - if exists already or not
        '''
        query = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_username = cursor.fetchone()
        return existing_username is not None


