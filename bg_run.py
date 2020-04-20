#!usr/bin/env python3
#Author: Ruslan Shakirov
#https://github.com/ruslanski/tech_news
#Start Date: 04/15/2020
#Telegram Bot
#Background File
import time
import bot

run = 0

def display():
    global run
    while 1:
        if run == 1:
            bot.runBot()
            print ("Telegram bot has been launched. Counting 30 min until new fetch..\n")
            time.sleep(3600)
            print ("30 min have passed. Time to update news\n\n")
            run = 0

