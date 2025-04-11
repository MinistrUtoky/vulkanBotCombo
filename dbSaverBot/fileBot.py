import time

import telebot
import codecs

from telegram.ext import Application, Updater, filters, MessageHandler
from dbmanager import DBManager

LIST_OF_ADMINS = [] # List of user_id of authorized users
LIST_OF_DB_ALLOWED_CHATS = []
ADMIN_NAMES = []
BOT_TOKEN = "skibidibop

bot = telebot.TeleBot(BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()
dbmanager = DBManager("data\\graphics_database.db")

def has_authority(message):
    if message.from_user.id in LIST_OF_ADMINS and message.from_user.username in ADMIN_NAMES:
        return True
    img = codecs.open('social_credit/nopower.gif', 'rb')
    bot.send_document(message.chat.id, img, None)
    img.close()
    return False

async def download_handler(update, context):
    if has_authority(update.message) and LIST_OF_DB_ALLOWED_CHATS.__contains__(update.message.chat.id):
        file = await context.bot.get_file(update.message.document)
        if dbmanager.is_model_format(update.message.document.file_name):
            table_name = "models"
        elif dbmanager.is_shader_format(update.message.document.file_name):
            table_name = "shaders"
        else:
            bot.send_message(update.message.chat.id,
                             "Inappropriate format. Please try again.", parse_mode="Markdown")
            return
        t = time.time()
        await file.download_to_drive("loaded\\" + update.message.document.file_name)
        dbmanager.insertFile("loaded\\" + update.message.document.file_name, table_name)
        t = time.time() - t
        bot.send_message(update.message.chat.id,
                         "Successfully downloaded, took " + str(round(t, 3)) + " seconds",
                         parse_mode="Markdown")

if __name__ == "__main__":
    application.add_handler(MessageHandler(filters.Document.ALL, download_handler))
    application.run_polling()
