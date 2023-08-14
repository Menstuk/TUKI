from colorama import Fore, Style

class Menu:
    def __init__(self):
        self.main_menu_logged_out_options = ['Sign Up', 'Sign In']
        self.main_menu_logged_in_options = ['Learning Mode', 'Test Mode', 'Sign Out']
    
    def print_main_menu_out(self):
        i = 1
        print(Fore.CYAN + Style.BRIGHT + "MAIN MENU")
        for item in self.main_menu_logged_out_options:
            print("    " + str(i) + ".", item)
            i += 1
        print("    0." , "Exit")
    
    def print_main_menu_in(self):
        i = 1
        print(Fore.CYAN + Style.BRIGHT + "MAIN MENU")
        for item in self.main_menu_logged_in_options:
            print("    " + str(i) + ".", item)
            i += 1
        print("    0." , "Exit")