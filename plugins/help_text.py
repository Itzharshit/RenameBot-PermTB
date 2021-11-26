import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import time
import os
import sqlite3
import asyncio

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import script

import pyrogram

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram.errors import UserNotParticipant

from plugins.rename_file import rename_doc


@Client.on_message(filters.command(["help"]))
def help_user(bot, update):
    bot.send_message(
        chat_id=update.chat.id,
        text=script.HELP_USER,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Subscribe Youtube", url="https://youtube.com/channel/UC2anvk7MNeNzJ6B4c0SZepw")]]),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["start"]))
def send_start(bot, update):
    # logger.info(update)
    
    bot.send_message(
        chat_id=update.chat.id,
        text=script.START_TEXT.format(update.from_user.first_name),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["upgrade"]))
def upgrade(bot, update):
    # logger.info(update)

    bot.send_message(
        chat_id=update.chat.id,
        text=script.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

    
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.voice | filters.video_note))
async def rename_cb(bot, update):
 
    file = update.document or update.video or update.audio or update.voice or update.video_note
    try:
        filename = file.file_name
    except:
        filename = "Not Available"
    
    await bot.send_message(
        chat_id=update.chat.id,
        text="<b>File Name</b> : <code>{}</code> \n\n𝗧𝗮𝗽 𝗼𝗻 𝗥𝗲𝗻𝗮𝗺𝗲 𝗯𝘂𝘁𝘁𝗼𝗻 𝘁𝗼 𝗿𝗲𝗻𝗮𝗺𝗲 𝘆𝗼𝘂𝗿 𝗳𝗶𝗹𝗲. ✍️".format(filename),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="𝗥𝗘𝗡𝗔𝗠𝗘 ✍️", callback_data="rename_button")],
                                                [InlineKeyboardButton(text="𝗖𝗔𝗡𝗖𝗟𝗘 ❌", callback_data="cancel_e")]]),
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True   
    )   


async def cancel_extract(bot, update):
    
    await bot.send_message(
        chat_id=update.chat.id,
        text="𝗬𝗼𝘂 𝗰𝗮𝗻𝗰𝗹𝗲𝗱 𝘁𝗵𝗲 𝗽𝗿𝗼𝗰𝗲𝘀𝘀.",
    )
