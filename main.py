#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telebot.image_editor import ImageEngine
from telebot.credentials import bot_token as TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

TOP_MSG_TXT = str()
BTM_MSG_TXT = str()
IMG = str()
MSG_IDS = list()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



PHOTO = 0

def addID(id):
    global MSG_IDS
    MSG_IDS.append(id)


def clearEverything():
    global TOP_MSG_TXT, BTM_MSG_TXT, IMG

    TOP_MSG_TXT = str()
    BTM_MSG_TXT = str()
    IMG = None
    MSG_IDS.clear()
    logger.info("Cleared Everthing!")


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about top message"""
    global TOP_MSG_TXT, BTM_MSG_TXT

    commands = update.message.text.replace("/bruh", "").split(';')
    try:
        top_msg = commands[0]
        bottom_msg = commands[1]
    except IndexError:
        update.message.reply_markdown_v2(
            'How to use: `/bruh <top message> ; <bottom message>`'
        )
        return ConversationHandler.END
    
    
    TOP_MSG_TXT = top_msg
    BTM_MSG_TXT = bottom_msg

    addID(update.message.message_id)
    update.message.reply_text(
        'Cool, now send me the meme template'
        'Send /cancel to stop talking to me.\n\n'
    )

    print(update.message.text)
    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo"""
    global IMG, TOP_MSG_TXT, BTM_MSG_TXT, MSG_IDS

    user = update.message.from_user
    IMG = update.message.photo[-1].get_file().file_path
    
    addID(update.message.message_id)
    logger.info("Photo of %s: %s", user.first_name, IMG)


    update.message.reply_text(
        'Gorgeous! Making the meme, please wait.'
    )
    
    Image = ImageEngine(TOP_MSG_TXT, BTM_MSG_TXT, "rc")
    file = Image.draw(IMG)
    
    bot = Bot(TOKEN)
    try:
        update.message.reply_photo(file, 'Hope you will like it!')
        for id in MSG_IDS:
            bot.delete_message(update.message.chat_id, id)

    except Exception as e:
        update.message.reply_text("I need delete message permission!")
        update.message.reply_text(e)
        clearEverything()
        return ConversationHandler.END
        
    clearEverything()
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    clearEverything()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('bruh', start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()