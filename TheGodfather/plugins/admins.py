import time
import asyncio
import html
from datetime import datetime, timedelta

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    Message, 
    ChatPermissions,
    ChatPrivileges
)

from pyrogram.errors import (
    UserAdminInvalid, 
    UsernameInvalid,
    UserNotParticipant,
    UsernameNotOccupied,
)

from config import PREFIX
from pyrogram import filters, Client



private = ("private", "bot")
def to_seconds(format, number): # number: int, format: s, m, h, d
    format_set = {"s": number, "m": number*60, "h": number*60*60, "d": number*60*60*24} 
    return int(format_set[format]) 



@Client.on_message(filters.command("ban", PREFIX) & filters.me)
async def ban_handler(app: Client, m: Message):
    try:
        if await app.check_private():
            return

        reply = m.reply_to_message
        user = False
        cmd = m.command
        ban_time = False

        if app.long() == 1 and not reply:
            return await app.send_edit("Reply or give some id | username after command.", text_type=["mono"], delme=4)

        if await app.IsAdmin("ban_users") is False:
            return await app.send_edit("You're not an admin here or you don't have enough admin rights.", text_type=["mono"], delme=4)

        if reply:
            user = await app.get_chat_member(m.chat.id, reply.from_user.id)
            if app.long() > 1:
                arg = cmd[1]
                ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

        elif not reply:
            if app.long() > 1:
                user = await app.get_chat_member(m.chat.id, cmd[1])
                if app.long() > 2:
                    arg = cmd[2]
                    ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

        if user:
            if user.user.is_self:
                return await app.send_edit("You can't ban yourself !", text_type=["mono"], delme=4)
            elif user.status == "administrator":
                return await app.send_edit("How am i supposed to ban an admin ?", text_type=["mono"], delme=4)
            elif user.status == "creator":
                return await app.send_edit("How am i supposed to ban a creator of a group ?", text_type=["mono"], delme=4)
        else:
            return await app.send_edit("Something went wrong !", text_type=["mono"], delme=4)

        await app.send_edit("⏳ • Hold on . . .", text_type=["mono"])
        if ban_time:
            await app.ban_chat_member(m.chat.id, user.user.id, datetime.now() + timedelta(ban_time))
            await app.send_edit(f"Banned {user.user.mention} for {arg}", delme=4)
        else:
            await app.ban_chat_member(m.chat.id, user.user.id)
            await app.send_edit(f"Banned {user.user.mention} in this chat.", delme=4)

    except (UsernameInvalid, UsernameNotOccupied):
        await app.send_edit("The provided username | id is invalid !", text_type=["mono"], delme=4)
    except UserNotParticipant:
        await app.send_edit("This user doesn't exist in this group !", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)






