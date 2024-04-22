import os
import sys
import time

import telebot
import requests
import math
from functools import wraps
import codecs

#import telegram.ext
#from telegram import Update, Bot
from telegram.ext import _application, _updater, filters, MessageHandler
import asyncio
from dbmanager import DBManager

LIST_OF_ADMINS = [572114691] # List of user_id of authorized users
LIST_OF_DB_ALLOWED_CHATS = [572114691]
ADMIN_NAMES = ["MinistrUtoky"]
BOT_TOKEN = "6318735982:AAEmvsHcoVAafpf9H805bNNqF0xRRqlMBaw"

bot = telebot.TeleBot(BOT_TOKEN)
application = _application.Application.builder().token(BOT_TOKEN).build()
dbmanager = DBManager("data\\graphics_database.db")

@bot.message_handler(commands=['add'])
def add_user_handler(message):
    if (has_authority(message)):
        text = "Write down users name"
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, username_handler)

@bot.message_handler(commands=['add_multiple'])
def add_multiple_users_handler(message):
    if (has_authority(message)):
        text = "Write down user names new line each with no spaces (first space indices end of a name)"
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, multiple_usernames_handler)

def username_handler(message):
    if (has_authority(message)):
        username = message.text
        with codecs.open('social_credit/social_credit.txt', encoding ='utf-16', mode ='r') as f:
            users = f.readlines()
        with codecs.open('social_credit/social_credit.txt', 'w', "utf-16") as f:
            users.append(username + " 100 social credit\n")
            f.writelines(users)
        bot.send_message(message.chat.id, "User succesfully added", parse_mode="Markdown")

def multiple_usernames_handler(message):
    if (has_authority(message)):
        usernames = message.text.split("\n")
        for u in usernames:
            u = u.split()[0]
            with codecs.open('social_credit/social_credit.txt', encoding='utf-16', mode='r') as f:
                users = f.readlines()
            with codecs.open('social_credit/social_credit.txt', 'w', "utf-16") as f:
                users.append(u + " 100 social credit\n")
                f.writelines(users)
        bot.send_message(message.chat.id, "Users succesfully added", parse_mode="Markdown")

@bot.message_handler(commands=['rep_list'])
def replist_handler(message):
    with codecs.open('social_credit/social_credit.txt', encoding ='utf-16', mode ='r') as f:
        text = ''.join(f.readlines())
        bot.send_message(message.chat.id, 'Current reputation list:\n'+text, parse_mode="Markdown")

@bot.message_handler(commands=['add_rep'])
def add_rep_handler(message):
    if (has_authority(message)):
        text = "Who's the party's pride and joy?"
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, user_rep_up_handler)

def user_rep_up_handler(message):
    if (has_authority(message)):
        username = message.text
        with codecs.open('social_credit/social_credit.txt', encoding ='utf-16', mode ='r') as f:
            users = f.readlines()
            exists = False
            for i in range(len(users)):
                if (users[i].split()[0] == username):
                    sc = int(users[i].split()[1])
                    sc = 1.1 * sc
                    if (sc>100):
                        sc=100
                    users[i] = username + " " + str(math.floor(sc)) + " social credit\n"
                    exists = True
            if not exists:
                bot.send_message(message.chat.id, "No such wangmin", parse_mode="Markdown")
                return
        with codecs.open('social_credit/social_credit.txt', 'w', "utf-16") as f:
            f.writelines(users)
        bot.send_message(message.chat.id, username + " recieves 0.5*{catwife} and 1*{bowl of rice}", parse_mode="Markdown")

@bot.message_handler(commands=['substract_rep'])
def substract_rep_handler(message):
    if (has_authority(message)):
        text = "Name, adress and fingerprints, please."
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, user_rep_down_handler)

@bot.message_handler(commands=['meow'])
def meow_handler(message):
    sent_msg = bot.send_message(message.chat.id, "Meow ฅ^•ﻌ•^ฅ", parse_mode="Markdown")

def user_rep_down_handler(message):
    if (has_authority(message)):
        username = message.text
        with codecs.open('social_credit/social_credit.txt', encoding ='utf-16', mode ='r') as f:
            users = f.readlines()
            exists = False
            for i in range(len(users)):
                if (users[i].split()[0] == username):
                    sc = int(users[i].split()[1])
                    sc = sc/1.1
                    users[i] = username + " " + str(math.floor(sc)) + " social credit\n"
                    exists = True
            if not exists:
                bot.send_message(message.chat.id, "No such wangmin", parse_mode="Markdown")
                return
        with codecs.open('social_credit/social_credit.txt', 'w', "utf-16") as f:
            f.writelines(users)
        bot.send_message(message.chat.id, username + " is now considered an uyghur and sentenced to the daily "
                                          "pork eating for the rest of eternity.", parse_mode="Markdown")

@bot.message_handler(commands=['clear'])
def clear_handler(message):
    if (has_authority(message)):
        with codecs.open('social_credit/social_credit.txt', 'w', "utf-16") as f:
            f.close()
        bot.send_message(message.chat.id, "Done.", parse_mode="Markdown")

@bot.message_handler(commands=['fillup'])
def load_data_handler(message):
    if (has_authority(message)):
        sent_msg = bot.send_message(message.chat.id, "Awaiting data.", parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, load_handler)

def load_handler(message):
        with codecs.open('social_credit/social_credit.txt', 'w', "utf-16") as f:
            f.write(message.text+'\n')
        bot.send_message(message.chat.id, "Lock and load!", parse_mode="Markdown")

def has_authority(message):
    if message.from_user.id in LIST_OF_ADMINS and message.from_user.username in ADMIN_NAMES:
        return True
    img = codecs.open('social_credit/nopower.gif', 'rb')
    bot.send_document(message.chat.id, img, None)
    img.close()
    return False
if __name__ == "__main__":
    bot.infinity_polling()
    with codecs.open('social_credit/social_credit.txt', encoding ='utf-16', mode ='r') as f:
        scinfo = f.readlines()
    with codecs.open('social_credit/social_credit_closeinfo.txt', 'w', "utf-16") as f:
        f.writelines(scinfo)
