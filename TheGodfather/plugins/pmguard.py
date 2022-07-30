from pyrogram import filters, Client
import asyncio

from pyrogram.methods import messages
from TheGodfather import CMD_HELP
from TheGodfather.helpers.pyrohelper import get_arg, denied_users
import TheGodfather.database.pmpermitdb as db
from config import PREFIX
from TheGodfather.plugins.pmpermit import *


@Client.on_message(filters.command("pmguard", PREFIX) & filters.me)
async def pmguard(app: Client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand on or off**")
        return
    if arg == "off":
        await db.set_pm(False)
        await message.edit("**PM Guard Deactivated**")
    if arg == "on":
        await db.set_pm(True)
        await message.edit("**PM Guard Activated**")

@Client.on_message(filters.command("setpmmsg", PREFIX) & filters.me)
async def setpmmsg(app: Client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        await db.set_permit_message(db.PMPERMIT_MESSAGE)
        await message.edit("**Anti_PM message set to default**.")
        return
    await db.set_permit_message(f"`{arg}`")
    await message.edit("**Custom anti-pm message set**")

@Client.on_message(filters.command(["allow", "ap", "approve", "a"], ["."]) & filters.me & filters.private)
async def allow(app: Client, message):
    chat_id = message.chat.id
    pmpermit, pm_message, limit, block_message = await db.get_pm_settings()
    await db.allow_user(chat_id)
    await message.edit(f"**I have allowed [you](tg://user?id={chat_id}) to PM me.**")
    async for message in app.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})
