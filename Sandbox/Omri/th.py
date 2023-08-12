import threading as th
import os
import time
import sys
import time
from termcolor import cprint, colored
def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')
keep_going = True

def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def do_stuff():
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    dots = 0
    while keep_going:
        print('\rRecording'+dots*'.', end='')
        time.sleep(1)
        dots += 1
        if dots == 4:
            dots = 0
import colorama
if __name__ == '__main__':
    print(colorama.Fore.RED + "Hello")

