"""Bhai Badd m multi Client kar dunga"""

from pyrogram import idle, Client, filters
from config import PREFIX
from TheGodfather import app, LOGGER
import logging
from TheGodfather.plugins import *

if app:
   app.start()
   me = app.get_me()
   print(f"UserBot started for user {me.id}. Type {PREFIX}help in any telegram chat.")
else:
   print("Plz add atleast one string Session")
idle()
