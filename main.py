#!usr/bin/env python3
#Author: Ruslan Shakirov
#https://github.com/ruslanski/tech_feedbot
#Start Date: 04/15/2020
#Telegram Bot
#main.py - Main File

from time import mktime
from datetime import datetime
import bot
import threading
import bg_run


t = threading.Thread(target=bg_run.display)
t.daemon = True
t.start()


while 1:
    if bg_run.run == 0:
        print("Initializing fetch of news-articles..\n")
        bot.scrape()
        print ("News-articles have been updated..\n")
        bg_run.run = 1
        
