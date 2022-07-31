"""Bhai Badd m multi Client kar dunga"""
import asyncio
import importlib
import os
import re
from pyrogram import idle, Client, filters
from config import PREFIX
from TheGodfather import app, LOGGER, bot
import logging
from rich.console import Console
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from rich.table import Table
from TheGodfather.plugins import ALL_MODULES
from config import LOG_CHAT

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
        if app:
           await app.start()
           print("Client 1 Has been Started 📂")
        else:
           print("Plz add atleast 1 SESSION")
        if bot:
           print("Booting Your Botfather Bot Token 📂")
           await bot.start()
        else:
           print("BOT_TOKEN has been not found Plz Add first")
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "TheGodfather.plugins." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
        try:
            await app.join_chat("TheGodfatherChat")
            await app.join_chat("GodfatherUserBot")
            await app.join_chat("The_Godfather_Network")
        except Exception as e:
            pass
        print("Your Userbot/ Assistant Bot has been Started Successfully ✨")
        await idle()



@bot.on_message(filters.command("start"))
async def alive(client: bot, m):
    reply_msg = f"**★彡[ʜᴇʏ! ɪ'ᴍ ꜱᴛɪʟʟ ᴀᴡᴀᴋᴇ!]彡★**\n"
    reply_msg += "\n📂 ꜱᴜᴘᴘᴏʀᴛ: [Click](https://t.me/TheGodfatherChat)\n📂 ᴄʜᴀɴɴᴇʟ: [Click](https://t.me/GodfatherUserBot)\n\n[**★彡[ᴘᴏᴡᴇʀᴇᴅ ʙʏ ɢᴏᴅꜰᴀᴛʜᴇʀ]彡★**](https://github.com/Team-TGN/Godfather)"
    photo = "https://telegra.ph/file/2c564b0cd45f8e39ef7e2.jpg"
    await m.delete()
    if m.reply_to_message:
        await client.send_photo(
            m.chat.id,
            photo,
            caption=reply_msg,
            reply_to_message_id=m.reply_to_message.message_id,
        )
    else:
        await client.send_photo(m.chat.id, photo, caption=reply_msg)



if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
