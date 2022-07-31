import logging
import sys
import time
from pyrogram import Client, errors
from config import API_HASH, API_ID, SESSION, BOT_TOKEN
import logging

import logging

logging.basicConfig(
    filename="app.txt",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
LOGGER = logging.getLogger(__name__)

HELP = {}
CMD_HELP = {}

StartTime = time.time()

if SESSION:
   app = Client(name="SESSION", api_id = API_ID, api_hash = API_HASH, session_string=SESSION, plugins=dict(root="TheGodfather.plugins"))
else:
   app = None

bot = Client(":memory:", API_ID, API_HASH, bot_token=BOT_TOKEN)
