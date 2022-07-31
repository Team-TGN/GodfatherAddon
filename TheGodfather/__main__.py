"""Bhai Badd m multi Client kar dunga"""
import asyncio
import importlib
import os
import re
from pyrogram import idle, Client, filters
from config import PREFIX
from TheGodfather import app, LOGGER, bot
import logging
from TheGodfather.plugins import *
from rich.console import Console
from rich.table import Table
from TheGodfather.plugins import ALL_MODULES

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
        if app:
           app.start()
           print("Client 1 Has been Started 📂")
        else:
           print("Plz add atleast 1 SESSION")
        if bot:
           print("Booting Your Botfather Bot Token 📂")
           bot.start()
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
            await app.join_chat("")
            await app.join_chat("")
        except:
            pass
        try:
            await app.send_message(
                LOG_CHAT,
                "<b>Heya Your Userbot Has been Started ✨</b>",
            )
        except Exception as e:
            print(
                "\nUserBot Account Has Failed To Access The Log Group.❗"
            )
        try:
            await bot.send_message(
                LOG_CHAT,
                "<b>🥀 Your Userbot/ Assistant Has been Started Successfully ✨</b>",
            )
        except Exception as e:
            print(
                "\nAssistant Bot Has Failed To Access The Log Group."
            )

if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
