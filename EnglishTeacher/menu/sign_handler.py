from colorama import Fore, Style

class Signing:
    def __init__(self):
        self.user_name = None
        

    def sign_up(self, db, cursor):
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Sign In>")
        user_name = input("Please enter your username: ")
        passwd = input("Please enter your password: ")
        
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (user_name, passwd))
        db.commit()
        print(user_name, "registered successfully")
        self.user_name = user_name
        return self.user_name
    
    def sign_in(self, db, cursor):
        log_in_flag = False
        while not log_in_flag: 
            print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "<Sign In>")
            user_name = input("Please enter your username: ")
            passwd = input("Please enter your password: ")
            
            select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(select_query, (user_name, passwd))
            
            if cursor.fetchone():
                print("Login successful.")
                log_in_flag = True
            else:
                print("Invalid username or password.")
                print("-------------------------------")
                print("1. Try Again")
                print("2. Exit")
                choice = int(input("Enter your choice:"))
                if choice == 2:
                    break
        if log_in_flag:
            self.user_name = user_name
        return log_in_flag, self.user_name

