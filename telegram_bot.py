from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import os
import os.path
from os import path
from pathlib import Path
import time
import logging
import random
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import ffmpy
import wikipedia
from translate import Translator
from langdetect import detect
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import asyncio
import csv
from datetime import datetime, timedelta, date
import smtplib

TOKEN = 'TOKEN'
glob_path = '/path/'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Making your day easier.\n\n Type /help for list of commands")

def wiki(update, context):
    search = context.args[0]
    summary = wikipedia.summary(search)
    summary_url = wikipedia.page(search).url
    context.bot.send_message(chat_id=update.effective_chat.id, text=summary + '\n\n' + summary_url)

def trad(update, context):
    language_out = context.args[0]

    language_in = detect(context.args[1])
    translator = Translator(to_lang=language_out, from_lang=language_in)
    translation = translator.translate(context.args[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text=translation)

def main():
    updater = Updater(token=TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('wiki', wiki))
    updater.dispatcher.add_handler(CommandHandler('trad', trad))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
