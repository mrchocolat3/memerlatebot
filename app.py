#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import json
import requests
import asyncio
from telebot.credentials import bot_token as TOKEN
from telebot.image_editor import ImageEngine
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def writeOnFile(update):
    json_string = update.to_json()
    stud_obj = json.loads(json_string)
    json.dump(stud_obj, open('file.json', 'w+'), indent=5)
    print("updated File")

# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!'
    )
    update.message.reply_text("Simply upload an image and the caption `/bruh` **top message** ; **bottom message**")
    
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def memer(update: Update, context: CallbackContext) -> None:
    writeOnFile(update)
    cmd = update.message.caption
    if cmd.startswith("/bruh"):
        if(update.message.photo):
            
            update.message.reply_markdown_v2(r"Making the meme\.\.\. " + update.effective_user.mention_markdown_v2())

            text = cmd.replace("/bruh", "").split(';')

            try:
                url = update.message.photo.pop().get_file(30).file_path
                Image = ImageEngine(text[0], text[1])

                file = Image.draw(url)
                # update.message.delete()
                update.message.reply_photo(file, 'Hope you like it!')

            except Exception as e:
                update.message.reply_markdown_v2(f"{update.effective_user.mention_markdown_v2()}"
                + f"\n**[ERROR]**: {e}"
                + "\n"
                + "\n**USAGE**: `/bruh top message ; bottom message`")

            # print(text)
        else:
            update.message.reply_text("Man just upload image, and do /bruh top text ; bottom text")
    else:
        update.message.reply_text("Man just upload image, and do /bruh top text ; bottom text")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(CommandHandler("bruh", memer))
    # # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.photo, memer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e) 
    
