"""
Copyright (C) 2022-2023 by Team-Tgn@Github, < https://github.com/Team-Tgn
By © https://github.com/ITZ-ZAID

All rights reserved.
"""

import asyncio
import random
import asyncio
import time
from typing import Tuple

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram import filters, Client
from traceback import format_exc
from typing import Tuple
ACTIVATE_LIST = []

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])





@Client.on_message(filters.me & filters.command(["aecho", "echo"], [".", "!"]))
async def gban(app: Client, message):
    Zaid = await message.reply_text("**Processing**")
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await Zaid.edit("**Whome should I Echo?**")
            return
    get_user = await app.get_users(user)
    elif int(get_user.id) in ACTIVATE_LIST:
        await Zaid.edit("Already echo activate in this user.")
        return
    ACTIVATE_LIST.append(get_user.id)
    await Zaid.edit(f"**Successfully Echo Started {get_user.first_name}!**")

@Client.on_message(filters.me & filters.command(["decho", "unecho", "rmecho"], [".", "!"]))
async def gbam(app: Client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.reply_text("**Whome should I rmEcho?**")
            return
    get_user = await app.get_users(user)
    ACTIVATE_LIST.remove(get_user.id)
    await message.reply_text(f"**Echo has Been Removed {get_user.first_name}, enjoy!**")


@Client.on_message(filters.text)
async def check_and_del(app: Client, message):
    if not message:
        return
    try:
        if not message.from_user.id in ACTIVATE_LIST:
            return
    except AttributeError:
        return
    message_id = message.message_id
    try:
        await message.reply_text(f"{message.text}")
    except:
        pass
