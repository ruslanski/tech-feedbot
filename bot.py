#!usr/bin/env python3
#Author: Ruslan Shakirov
#https://github.com/ruslanski/tech_feedbot
#Start Date: 04/15/2020
#Telegram Bot

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import RegexHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from string import ascii_lowercase
from string import digits
from random import choice
from sys import exc_info as error
import pandas as pd
import feedparser as fp
import json
import newspaper
from newspaper import Article
from time import gmtime, strftime, mktime
import socket
import logging
import time
import threading
from datetime import datetime
def runBot():
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    NEWS, ABOUT = range(2)

    ############################### START ############################################
    def start(bot,update):
        user = update.message.from_user
        reply_keyboard = [['Start'],['']]
        update.message.reply_text(text="\U0001F4BC Hello, "+format(user.first_name)+' '+format(user.last_name)+'! '+"Welcome to @Tech-Feed Bot.\n\n\U0001F5A8 Click on the button below to start.\n",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return NEWS
    ############################### FIRST-MENU SOURCES ############################################
    def first_menu(bot,update):
        user = update.message.from_user
        logger.info("Name: %s %s | Username: %s | Clicked on: %s", user.first_name, user.last_name, user.username, update.message.text)
        update.message.reply_text('\U0001F6CE Congratulations! You are subscribed.\n\n\U0001F4C1 Each source displays 10 latest articles and updates every 30 min.\n\n\U0001F447 Pick a source below or type /cancel', 
                              reply_markup=first_menu_keyboard())

    def first_menu_keyboard():
        keyboard = [[InlineKeyboardButton('TechCrunch.com', callback_data='m1_1'),InlineKeyboardButton('TheNextWeb.com', callback_data='m1_2')],
                    [InlineKeyboardButton('Droid-life.com', callback_data='m1_3'),InlineKeyboardButton('Gizmodo.com', callback_data='m1_4')],
                     [InlineKeyboardButton('Firstpost.com', callback_data='m1_5'),InlineKeyboardButton('TheVerge.com', callback_data='m1_6')],
                    [InlineKeyboardButton('Slashgear.com', callback_data='m1_7'),InlineKeyboardButton('Engadget.com', callback_data='m1_8')],
                       [InlineKeyboardButton('DigitalTrends.com', callback_data='m1_9'),InlineKeyboardButton('Macrumors.com', callback_data='m1_10')],
                    [InlineKeyboardButton('VentureBeat.com', callback_data='m1_11'),InlineKeyboardButton('Playstation', callback_data='m1_12')]]
        return InlineKeyboardMarkup(keyboard)
    ############################### SECOND-MENU ############################################

    def main_menu(bot, update):
          query = update.callback_query
          bot.edit_message_text(chat_id=query.message.chat_id, 
                              message_id=query.message.message_id,
                              text='\U0001F590 Hello, welcome to @Tech-News Bot! \U0001F6CE You are subscribed.\n\n\U0001F4C1 Each source displays 10 latest articles and updates every 30 min.\n\n'+'\U0001F447 Pick a source below or type /cancel', 
                              reply_markup = main_menu_keyboard(),
                              parse_mode="Markdown")

    def main_menu_keyboard():
        keyboard = [[InlineKeyboardButton('TechCrunch.com', callback_data='m1_1'),InlineKeyboardButton('TheNextWeb.com', callback_data='m1_2')],
                    [InlineKeyboardButton('Droid-life.com', callback_data='m1_3'),InlineKeyboardButton('Gizmodo.com', callback_data='m1_4')],
                     [InlineKeyboardButton('Firstpost.com', callback_data='m1_5'),InlineKeyboardButton('TheVerge.com', callback_data='m1_6')],
                    [InlineKeyboardButton('Slashgear.com', callback_data='m1_7'),InlineKeyboardButton('Engadget.com', callback_data='m1_8')],
                       [InlineKeyboardButton('DigitalTrends.com', callback_data='m1_9'),InlineKeyboardButton('Macrumors.com', callback_data='m1_10')],
                    [InlineKeyboardButton('VentureBeat.com', callback_data='m1_11'),InlineKeyboardButton('Playstation', callback_data='m1_12')]]
        return InlineKeyboardMarkup(keyboard)




    ############################### SUBMENU_BUTTON ############################################ 
    def submenu_button(u1,u2):
        keyboard = [[InlineKeyboardButton('Back', callback_data=u1),InlineKeyboardButton('Next', callback_data=u2)],
                    [InlineKeyboardButton('Sources', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    def submenu_button_final(u1,u2):
        keyboard = [[InlineKeyboardButton('Back', callback_data=u1),InlineKeyboardButton('Next Source', callback_data=u2)],
                    [InlineKeyboardButton('Main Menu', callback_data="main")]]
        return InlineKeyboardMarkup(keyboard)

    ############################### FIRST_SUBMENU ############################################   

    def first_submenu(bot, update):
        #user = update.message.from_user
        #logger.info("Name: %s %s | Username: %s | Clicked on: %s", user.first_name, user.last_name, user.username, update.message.text)
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id, 
                              message_id=query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(0,'techcrunch.com')+")",
                              reply_markup = submenu_button("main","sm1_1"),
                              parse_mode="Markdown")

    def first_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(1,'techcrunch.com')+")",
                              reply_markup = submenu_button("m1_1","sm1_2"),
                              parse_mode="Markdown")

    def first_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(2,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_1","sm1_3"),
                              parse_mode="Markdown")

    def first_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(3,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_2","sm1_4"),
                              parse_mode="Markdown")

    def first_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(4,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_3","sm1_5"),
                              parse_mode="Markdown")

    def first_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(5,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_4","sm1_6"),
                              parse_mode="Markdown")
                              
    def first_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(6,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_5","sm1_7"),
                              parse_mode="Markdown")

    def first_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(7,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_6","sm1_8"),
                              parse_mode="Markdown")

    def first_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(8,'techcrunch.com')+")",
                              reply_markup = submenu_button("sm1_7","sm1_9"),
                              parse_mode="Markdown")

    def first_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from techcrunch.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(9,'techcrunch.com')+")",
                              reply_markup = submenu_button_final("sm1_8","m1_2"),
                              parse_mode="Markdown")    

    #############################################SECOND_SUBMENU#######################################################

    def second_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(0,'thenextweb.com')+")",
                              reply_markup = submenu_button("main","sm2_1"),
                              parse_mode="Markdown")

    def second_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(1,'thenextweb.com')+")",
                              reply_markup = submenu_button("m1_2","sm2_2"),
                              parse_mode="Markdown")

    def second_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(2,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_1","sm2_3"),
                              parse_mode="Markdown")

    def second_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(3,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_2","sm2_4"),
                              parse_mode="Markdown")

    def second_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(4,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_3","sm2_5"),
                              parse_mode="Markdown")

    def second_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(5,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_4","sm2_6"),
                              parse_mode="Markdown")

    def second_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(6,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_5","sm2_7"),
                              parse_mode="Markdown")

    def second_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(7,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_6","sm2_8"),
                              parse_mode="Markdown")

    def second_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(8,'thenextweb.com')+")",
                              reply_markup = submenu_button("sm2_7","sm2_9"),
                              parse_mode="Markdown")

    def second_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from thenextweb.com\n\n  \U0001F449 [ Read the article...]("+newsmessage(9,'thenextweb.com')+")",
                              reply_markup = submenu_button_final("sm2_8","m1_3"),
                              parse_mode="Markdown")



      #####################################THIRD_SUBMENU#############################
    def third_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'droid-life.com')+")",
                              reply_markup = submenu_button("main","sm3_1"),
                              parse_mode="Markdown")

    def third_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'droid-life.com')+")",
                              reply_markup = submenu_button("m1_3","sm3_2"),
                              parse_mode="Markdown")

    def third_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_1","sm3_3"),
                              parse_mode="Markdown")


    def third_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_2","sm3_4"),
                              parse_mode="Markdown")

    def third_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_3","sm3_5"),
                              parse_mode="Markdown")

    def third_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_4","sm3_6"),
                              parse_mode="Markdown")

    def third_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_5","sm3_7"),
                              parse_mode="Markdown")

    def third_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_6","sm3_8"),
                              parse_mode="Markdown")

    def third_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'droid-life.com')+")",
                              reply_markup = submenu_button("sm3_7","sm3_9"),
                              parse_mode="Markdown")

    def third_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from droid-life.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'droid-life.com')+")",
                              reply_markup = submenu_button_final("sm3_8","m1_4"),
                              parse_mode="Markdown")


      ############################ fourth SUBMENU #########################################

    def fourth_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'gizmodo.com')+")",
                              reply_markup = submenu_button("main","sm4_1"),
                              parse_mode="Markdown")

    def fourth_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'gizmodo.com')+")",
                              reply_markup = submenu_button("m1_4","sm4_2"),
                              parse_mode="Markdown")

    def fourth_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_1","sm4_3"),
                              parse_mode="Markdown")

    def fourth_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_2","sm4_4"),
                              parse_mode="Markdown")

    def fourth_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_3","sm4_5"),
                              parse_mode="Markdown")

    def fourth_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_4","sm4_6"),
                              parse_mode="Markdown")

    def fourth_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_5","sm4_7"),
                              parse_mode="Markdown")

    def fourth_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_6","sm4_8"),
                              parse_mode="Markdown")

    def fourth_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'gizmodo.com')+")",
                              reply_markup = submenu_button("sm4_7","sm4_9"),
                              parse_mode="Markdown")

    def fourth_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from gizmodo.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'gizmodo.com')+")",
                              reply_markup = submenu_button_final("sm4_8","m1_5"),
                              parse_mode="Markdown")
        
      ############################ Fifth Submenu #######################################
    def fifth_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'firstpost.com')+")",
                              reply_markup = submenu_button("main","sm5_1"),
                              parse_mode="Markdown")

    def fifth_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'firstpost.com')+")",
                              reply_markup = submenu_button("m1_5","sm5_2"),
                              parse_mode="Markdown")

    def fifth_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_1","sm5_3"),
                              parse_mode="Markdown")

    def fifth_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_2","sm5_4"),
                              parse_mode="Markdown")

    def fifth_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_3","sm5_5"),
                              parse_mode="Markdown")

    def fifth_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_4","sm5_6"),
                              parse_mode="Markdown")

    def fifth_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_5","sm5_7"),
                              parse_mode="Markdown")

    def fifth_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_6","sm5_8"),
                              parse_mode="Markdown")

    def fifth_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'firstpost.com')+")",
                              reply_markup = submenu_button("sm5_7","sm5_9"),
                              parse_mode="Markdown")

    def fifth_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from firstpost.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'firstpost.com')+")",
                              reply_markup = submenu_button_final("sm5_8","m1_6"),
                              parse_mode="Markdown")
      #####################################SIXTH SUBMENU########################################
    def sixth_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'theverge.com')+")",
                              reply_markup = submenu_button("main","sm6_1"),
                              parse_mode="Markdown")

    def sixth_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'theverge.com')+")",
                              reply_markup = submenu_button("m1_6","sm6_2"),
                              parse_mode="Markdown")

    def sixth_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_1","sm6_3"),
                              parse_mode="Markdown")

    def sixth_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_2","sm6_4"),
                              parse_mode="Markdown")

    def sixth_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_3","sm6_5"),
                              parse_mode="Markdown")

    def sixth_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_4","sm6_6"),
                              parse_mode="Markdown")
                              
    def sixth_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_5","sm6_7"),
                              parse_mode="Markdown")

    def sixth_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_6","sm6_8"),
                              parse_mode="Markdown")

    def sixth_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'theverge.com')+")",
                              reply_markup = submenu_button("sm6_7","sm6_9"),
                              parse_mode="Markdown")

    def sixth_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from TheVerge.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'theverge.com')+")",
                              reply_markup = submenu_button_final("sm6_8","m1_7"),
                              parse_mode="Markdown")

      #############################################SEVENTH_SUBMENU#######################################################

    def seventh_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'slashgear.com')+")",
                              reply_markup = submenu_button("main","sm7_1"),
                              parse_mode="Markdown")

    def seventh_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'slashgear.com')+")",
                              reply_markup = submenu_button("m1_7","sm7_2"),
                              parse_mode="Markdown")

    def seventh_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_1","sm7_3"),
                              parse_mode="Markdown")

    def seventh_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_2","sm7_4"),
                              parse_mode="Markdown")

    def seventh_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_3","sm7_5"),
                              parse_mode="Markdown")

    def seventh_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_4","sm7_6"),
                              parse_mode="Markdown")

    def seventh_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_5","sm7_7"),
                              parse_mode="Markdown")

    def seventh_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_6","sm7_8"),
                              parse_mode="Markdown")

    def seventh_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'slashgear.com')+")",
                              reply_markup = submenu_button("sm7_7","sm7_9"),
                              parse_mode="Markdown")

    def seventh_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Slashgear.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'slashgear.com')+")",
                              reply_markup = submenu_button_final("sm7_8","m1_8"),
                              parse_mode="Markdown")



      #####################################EIGHTS_SUBMENU#############################
    def eights_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'engadget.com')+")",
                              reply_markup = submenu_button("main","sm8_1"),
                              parse_mode="Markdown")

    def eights_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'engadget.com')+")",
                              reply_markup = submenu_button("m1_8","sm8_2"),
                              parse_mode="Markdown")

    def eights_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_1","sm8_3"),
                              parse_mode="Markdown")


    def eights_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_2","sm8_4"),
                              parse_mode="Markdown")

    def eights_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_3","sm8_5"),
                              parse_mode="Markdown")

    def eights_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_4","sm8_6"),
                              parse_mode="Markdown")

    def eights_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_5","sm8_7"),
                              parse_mode="Markdown")

    def eights_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_6","sm8_8"),
                              parse_mode="Markdown")

    def eights_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'engadget.com')+")",
                              reply_markup = submenu_button("sm8_7","sm8_9"),
                              parse_mode="Markdown")

    def eights_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Engadget.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'engadget.com')+")",
                              reply_markup = submenu_button_final("sm8_8","m1_9"),
                              parse_mode="Markdown")
      #############################################NINETH_SUBMENU#######################################################

    def nineth_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'digitaltrends.com')+")",
                              reply_markup = submenu_button("main","sm9_1"),
                              parse_mode="Markdown")

    def nineth_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'digitaltrends.com')+")",
                              reply_markup = submenu_button("m1_9","sm9_2"),
                              parse_mode="Markdown")

    def nineth_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_1","sm9_3"),
                              parse_mode="Markdown")

    def nineth_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_2","sm9_4"),
                              parse_mode="Markdown")

    def nineth_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_3","sm9_5"),
                              parse_mode="Markdown")

    def nineth_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_4","sm9_6"),
                              parse_mode="Markdown")

    def nineth_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_5","sm9_7"),
                              parse_mode="Markdown")

    def nineth_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_6","sm9_8"),
                              parse_mode="Markdown")

    def nineth_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'digitaltrends.com')+")",
                              reply_markup = submenu_button("sm9_7","sm9_9"),
                              parse_mode="Markdown")

    def nineth_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from DigitalTrends.comm\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'digitaltrends.com')+")",
                              reply_markup = submenu_button_final("sm9_8","m1_10"),
                              parse_mode="Markdown")



      #####################################TENTH_SUBMENU#############################
    def tenth_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'macrumors.com')+")",
                              reply_markup = submenu_button("main","sm10_1"),
                              parse_mode="Markdown")

    def tenth_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'macrumors.com')+")",
                              reply_markup = submenu_button("m1_10","sm10_2"),
                              parse_mode="Markdown")

    def tenth_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_1","sm10_3"),
                              parse_mode="Markdown")


    def tenth_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_2","sm10_4"),
                              parse_mode="Markdown")

    def tenth_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_3","sm10_5"),
                              parse_mode="Markdown")

    def tenth_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_4","sm10_6"),
                              parse_mode="Markdown")

    def tenth_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_5","sm10_7"),
                              parse_mode="Markdown")

    def tenth_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_6","sm10_8"),
                              parse_mode="Markdown")

    def tenth_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'macrumors.com')+")",
                              reply_markup = submenu_button("sm10_7","sm10_9"),
                              parse_mode="Markdown")

    def tenth_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Macrumors.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'macrumors.com')+")",
                              reply_markup = submenu_button_final("sm10_8","m1_11"),
                              parse_mode="Markdown")
      #############################################ELEVENTH_SUBMENU#######################################################

    def eleventh_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'venturebeat.com')+")",
                              reply_markup = submenu_button("main","sm11_1"),
                              parse_mode="Markdown")

    def eleventh_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'venturebeat.com')+")",
                              reply_markup = submenu_button("m1_11","sm11_2"),
                              parse_mode="Markdown")

    def eleventh_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_1","sm11_3"),
                              parse_mode="Markdown")

    def eleventh_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_2","sm11_4"),
                              parse_mode="Markdown")

    def eleventh_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_3","sm11_5"),
                              parse_mode="Markdown")

    def eleventh_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_4","sm11_6"),
                              parse_mode="Markdown")

    def eleventh_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_5","sm11_7"),
                              parse_mode="Markdown")

    def eleventh_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_6","sm11_8"),
                              parse_mode="Markdown")

    def eleventh_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'venturebeat.com')+")",
                              reply_markup = submenu_button("sm11_7","sm11_9"),
                              parse_mode="Markdown")

    def eleventh_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from venturebeat.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'venturebeat.com')+")",
                              reply_markup = submenu_button_final("sm11_8","m1_12"),
                              parse_mode="Markdown")

      #####################################TWELVETH_SUBMENU#############################
    def twelveth_submenu(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(0,'playstation.com')+")",
                              reply_markup = submenu_button("main","sm12_1"),
                              parse_mode="Markdown")

    def twelveth_submenu01(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(1,'playstation.com')+")",
                              reply_markup = submenu_button("m1_12","sm12_2"),
                              parse_mode="Markdown")

    def twelveth_submenu02(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(2,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_1","sm12_3"),
                              parse_mode="Markdown")


    def twelveth_submenu03(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(3,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_2","sm12_4"),
                              parse_mode="Markdown")

    def twelveth_submenu04(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(4,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_3","sm12_5"),
                              parse_mode="Markdown")

    def twelveth_submenu05(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(5,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_4","sm12_6"),
                              parse_mode="Markdown")

    def twelveth_submenu06(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(6,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_5","sm12_7"),
                              parse_mode="Markdown")

    def twelveth_submenu07(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(7,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_6","sm12_8"),
                              parse_mode="Markdown")

    def twelveth_submenu08(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(8,'playstation.com')+")",
                              reply_markup = submenu_button("sm12_7","sm12_9"),
                              parse_mode="Markdown")

    def twelveth_submenu09(bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id = query.message.message_id,
                              text="News from Playstation.com\n\n  \U0001F449 [ Read more...]("+newsmessage(9,'playstation.com')+")",
                              reply_markup = submenu_button_final("sm12_8","m1"),
                              parse_mode="Markdown")
    ############################### Read from JSON ############################################   
    def newsmessage(art,source):
        """
        Listing objects with .json format
            for key, source in dict_train.items():
                for i in value["URL"]:
                    newList.append(i)
                    print(newList)
            for x in range(len(newList)):
                print(newList[i+art])
                return newList[i+art]
        """
        file = 'articles.json'
         # converting json dataset from dictionary to dataframe
        with open(file, 'r', encoding="utf-8") as train_file:
          dict_train = json.load(train_file)
        df = pd.DataFrame.from_dict(dict_train, orient='index')
        df.reset_index(level=0, inplace=True)
        df["companies"]=df["index"]
        df2 = df.set_index(['companies'])['articles'].apply(pd.Series).stack()
        df2 = df2.reset_index()
        df2.columns = ['companies','articles','article']
        df2 = df2[["companies","article"]]
        df2 = pd.concat([df2.drop('article', axis=1), pd.DataFrame(df2['article'].tolist())], axis=1)
        df3 = df2[['companies','link','published','title']]
        newList = df3.loc[df3["companies"] == source]['link'].values

        for i in range(len(newList)):

          return (newList[i+art])
        file.close()
    ########################### OTHER COMMANDS #########################################
    def cancel(bot,update):
        user = update.message.from_user
        logger.info("Name: %s %s | Username: %s | Clicked on: %s", user.first_name, user.last_name, user.username, update.message.text)
        update.message.reply_text('Sorry to see you go! Type /start to launch the bot.',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def error(update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)



    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    
    updater = Updater("API-KEY")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='^main$'))
    dp.add_handler(CallbackQueryHandler(first_submenu, pattern='^m1_1$'))
    dp.add_handler(CallbackQueryHandler(first_submenu01, pattern='^sm1_1$'))
    dp.add_handler(CallbackQueryHandler(first_submenu02, pattern='^sm1_2$'))
    dp.add_handler(CallbackQueryHandler(first_submenu03, pattern='^sm1_3$'))
    dp.add_handler(CallbackQueryHandler(first_submenu04, pattern='^sm1_4$'))
    dp.add_handler(CallbackQueryHandler(first_submenu05, pattern='^sm1_5$'))
    dp.add_handler(CallbackQueryHandler(first_submenu06, pattern='^sm1_6$'))
    dp.add_handler(CallbackQueryHandler(first_submenu07, pattern='^sm1_7$'))
    dp.add_handler(CallbackQueryHandler(first_submenu08, pattern='^sm1_8$'))
    dp.add_handler(CallbackQueryHandler(first_submenu09, pattern='^sm1_9$'))
    
    dp.add_handler(CallbackQueryHandler(second_submenu, pattern='^m1_2$'))
    dp.add_handler(CallbackQueryHandler(second_submenu01, pattern='^sm2_1$'))
    dp.add_handler(CallbackQueryHandler(second_submenu02, pattern='^sm2_2$'))
    dp.add_handler(CallbackQueryHandler(second_submenu03, pattern='^sm2_3$'))
    dp.add_handler(CallbackQueryHandler(second_submenu04, pattern='^sm2_4$'))
    dp.add_handler(CallbackQueryHandler(second_submenu05, pattern='^sm2_5$'))
    dp.add_handler(CallbackQueryHandler(second_submenu06, pattern='^sm2_6$'))
    dp.add_handler(CallbackQueryHandler(second_submenu07, pattern='^sm2_7$'))
    dp.add_handler(CallbackQueryHandler(second_submenu08, pattern='^sm2_8$'))
    dp.add_handler(CallbackQueryHandler(second_submenu09, pattern='^sm2_9$'))

    dp.add_handler(CallbackQueryHandler(third_submenu, pattern='^m1_3$'))
    dp.add_handler(CallbackQueryHandler(third_submenu01, pattern='^sm3_1$'))
    dp.add_handler(CallbackQueryHandler(third_submenu02, pattern='^sm3_2$'))
    dp.add_handler(CallbackQueryHandler(third_submenu03, pattern='^sm3_3$'))
    dp.add_handler(CallbackQueryHandler(third_submenu04, pattern='^sm3_4$'))
    dp.add_handler(CallbackQueryHandler(third_submenu05, pattern='^sm3_5$'))
    dp.add_handler(CallbackQueryHandler(third_submenu06, pattern='^sm3_6$'))
    dp.add_handler(CallbackQueryHandler(third_submenu07, pattern='^sm3_7$'))
    dp.add_handler(CallbackQueryHandler(third_submenu08, pattern='^sm3_8$'))
    dp.add_handler(CallbackQueryHandler(third_submenu09, pattern='^sm3_9$'))

    dp.add_handler(CallbackQueryHandler(fourth_submenu, pattern='^m1_4$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu01, pattern='^sm4_1$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu02, pattern='^sm4_2$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu03, pattern='^sm4_3$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu04, pattern='^sm4_4$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu05, pattern='^sm4_5$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu06, pattern='^sm4_6$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu07, pattern='^sm4_7$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu08, pattern='^sm4_8$'))
    dp.add_handler(CallbackQueryHandler(fourth_submenu09, pattern='^sm4_9$'))

    dp.add_handler(CallbackQueryHandler(fifth_submenu, pattern='^m1_5$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu01, pattern='^sm5_1$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu02, pattern='^sm5_2$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu03, pattern='^sm5_3$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu04, pattern='^sm5_4$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu05, pattern='^sm5_5$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu06, pattern='^sm5_6$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu07, pattern='^sm5_7$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu08, pattern='^sm5_8$'))
    dp.add_handler(CallbackQueryHandler(fifth_submenu09, pattern='^sm5_9$'))

    dp.add_handler(CallbackQueryHandler(sixth_submenu, pattern='^m1_6$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu01, pattern='^sm6_1$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu02, pattern='^sm6_2$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu03, pattern='^sm6_3$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu04, pattern='^sm6_4$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu05, pattern='^sm6_5$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu06, pattern='^sm6_6$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu07, pattern='^sm6_7$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu08, pattern='^sm6_8$'))
    dp.add_handler(CallbackQueryHandler(sixth_submenu09, pattern='^sm6_9$'))

    dp.add_handler(CallbackQueryHandler(seventh_submenu, pattern='^m1_7$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu01, pattern='^sm7_1$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu02, pattern='^sm7_2$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu03, pattern='^sm7_3$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu04, pattern='^sm7_4$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu05, pattern='^sm7_5$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu06, pattern='^sm7_6$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu07, pattern='^sm7_7$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu08, pattern='^sm7_8$'))
    dp.add_handler(CallbackQueryHandler(seventh_submenu09, pattern='^sm7_9$'))

    dp.add_handler(CallbackQueryHandler(eights_submenu, pattern='^m1_8$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu01, pattern='^sm8_1$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu02, pattern='^sm8_2$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu03, pattern='^sm8_3$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu04, pattern='^sm8_4$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu05, pattern='^sm8_5$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu06, pattern='^sm8_6$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu07, pattern='^sm8_7$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu08, pattern='^sm8_8$'))
    dp.add_handler(CallbackQueryHandler(eights_submenu09, pattern='^sm8_9$'))

    dp.add_handler(CallbackQueryHandler(nineth_submenu, pattern='^m1_9$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu01, pattern='^sm9_1$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu02, pattern='^sm9_2$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu03, pattern='^sm9_3$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu04, pattern='^sm9_4$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu05, pattern='^sm9_5$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu06, pattern='^sm9_6$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu07, pattern='^sm9_7$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu08, pattern='^sm9_8$'))
    dp.add_handler(CallbackQueryHandler(nineth_submenu09, pattern='^sm9_9$'))

    dp.add_handler(CallbackQueryHandler(tenth_submenu, pattern='^m1_10$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu01, pattern='^sm10_1$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu02, pattern='^sm10_2$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu03, pattern='^sm10_3$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu04, pattern='^sm10_4$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu05, pattern='^sm10_5$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu06, pattern='^sm10_6$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu07, pattern='^sm10_7$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu08, pattern='^sm10_8$'))
    dp.add_handler(CallbackQueryHandler(tenth_submenu09, pattern='^sm10_9$'))

    dp.add_handler(CallbackQueryHandler(eleventh_submenu, pattern='^m1_11$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu01, pattern='^sm11_1$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu02, pattern='^sm11_2$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu03, pattern='^sm11_3$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu04, pattern='^sm11_4$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu05, pattern='^sm11_5$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu06, pattern='^sm11_6$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu07, pattern='^sm11_7$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu08, pattern='^sm11_8$'))
    dp.add_handler(CallbackQueryHandler(eleventh_submenu09, pattern='^sm11_9$'))

    dp.add_handler(CallbackQueryHandler(twelveth_submenu, pattern='^m1_12$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu01, pattern='^sm12_1$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu02, pattern='^sm12_2$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu03, pattern='^sm12_3$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu04, pattern='^sm12_4$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu05, pattern='^sm12_5$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu06, pattern='^sm12_6$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu07, pattern='^sm12_7$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu08, pattern='^sm12_8$'))
    dp.add_handler(CallbackQueryHandler(twelveth_submenu09, pattern='^sm12_9$'))
    # Add conversation handler with the states SOURCE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={NEWS: [MessageHandler(Filters.regex('^(Start)$'), first_menu)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    
def scrape():
  LIMIT = 10
  data = {}
  data_file ="""{
 "techcrunch.com":
          {"rss": "https://techcrunch.com/feed/",
           "link": "https://techcrunch.com/"},
      "thenextweb.com":
          {"rss": "http://feeds2.feedburner.com/thenextweb/",
          "link": "https://thenextweb.com/"},
      "droid-life.com":
          {"rss": "https://www.droid-life.com/rss",
           "link": "https://www.droid-life.com/"},
      "gizmodo.com":
          {"rss": "https://gizmodo.com/rss",
           "link": "https://gizmodo.com/"},
      "firstpost.com":
          {"rss": "https://www.firstpost.com/rss/tech-news-feed.xml",
           "link": "https://www.firstpost.com/tech/"},
      "theverge.com":
          {"rss": "https://www.theverge.com/rss/front-page/index.xml",
           "link": "www.theverge.com"},
      "slashgear.com":
          {"rss": "https://www.slashgear.com/feed/",
           "link": "https://www.slashgear.com/"},
      "engadget.com":
          {"rss": "https://www.engadget.com/rss.xml",
           "link": "https://www.engadget.com/"},
      "digitaltrends.com":
          {"rss": "https://www.digitaltrends.com/feed/",
           "link": "https://www.digitaltrends.com/"},
      "macrumors.com":
          {"rss": "http://feeds.macrumors.com/MacRumors-All",
           "link": "https://www.macrumors.com/"},
      "venturebeat.com":
          {"rss": "https://feeds.feedburner.com/venturebeat/SZYF",
           "link": "https://venturebeat.com/"},
      "playstation.com":
          {"rss": "http://feeds.feedburner.com/psblog",
           "link": "https://blog.us.playstation.com/"}
          
  }"""

  companies = json.loads(data_file)
  count = 1
  # Iterate through each news company
  for company, value in companies.items():
      # If a RSS link is provided in the JSON file, this will be the first choice.
      # Reason for this is that, RSS feeds often give more consistent and correct data.
      # If you do not want to scrape from the RSS-feed, just leave the RSS attr empty in the JSON file.
      if 'rss' in value:
          d = fp.parse(value['rss'])
          print("Downloading articles from ", company)
          newsPaper = {
              "rss": value['rss'],
              "link": value['link'],
              "articles": []
          }
          for entry in d.entries:
              # Check if publish date is provided, if no the article is skipped.
              # This is done to keep consistency in the data and to keep the script from crashing.
              if hasattr(entry, 'published'):
                  if count > LIMIT:
                      break
                  article = {}
                  article['link'] = entry.link
                  date = entry.published_parsed
                  article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                  try:
                      content = Article(entry.link)
                      content.download()
                      content.parse()
                  except Exception as e:
                      # If the download for some reason fails (ex. 404) the script will continue downloading
                      # the next article.
                      print(e)
                      print("continuing...")
                      continue
                  article['title'] = content.title
                  #article['text'] = content.text
                  newsPaper['articles'].append(article)
                  #print(count, "articles downloaded from", company, "\n URL: ", entry.link)
                  count = count + 1
      else:
          # This is the fallback method if a RSS-feed link is not provided.
          # It uses the python newspaper library to extract articles
          print("\n Building site for ", company)
          paper = newspaper.build(value['link'], memoize_articles=False)
          newsPaper = {
              "link": value['link'],
              "articles": []
          }
          noneTypeCount = 0
          for content in paper.articles:
              if count > LIMIT:
                  break
              try:
                  content.download()
                  content.parse()
              except Exception as e:
                  print(e)
                  print("continuing...")
                  continue
              # Again, for consistency, if there is no found publish date the article will be skipped.
              # After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.
              if content.publish_date is None:
                  print(count, " Article has date of type None...")
                  noneTypeCount = noneTypeCount + 1
                  if noneTypeCount > 10:
                      print("Too many noneType dates, aborting...")
                      noneTypeCount = 0
                      break
                  count = count + 1
                  continue
              article = {}
              #article['title'] = content.title
              #article['text'] = content.text
              article['link'] = content.url
              article['published'] = content.publish_date.isoformat()
              newsPaper['articles'].append(article)
              #print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
              count = count + 1
              noneTypeCount = 0
          [x.encode("utf-8") for x in newsPaper]
      count = 1
      data[company] = newsPaper
      
  #json.dumps(obj, ensure_ascii=False
  # Finally it saves the articles as a JSON-file.
  try:
      with open('articles.json', 'w', encoding="utf-8") as outfile:
          json.dump(data, outfile, ensure_ascii=False)
          print ("Saved to json\n")
  except Exception as e:
      print(e)
  finally:
    outfile.close()
