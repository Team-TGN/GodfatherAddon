import asyncio
from datetime import datetime

from pyrogram import filters, Client
from pyrogram.errors import PeerIdInvalid
from pyrogram.raw import functions
from pyrogram.types import Message, User
from config import PREFIX
from TheGodfather.helpers.PyroHelpers import ReplyCheck
from TheGodfather.plugins.info import *


@Client.on_message(filters.command(["whois", "info"], PREFIX) & filters.me)
async def who_is(bot: Client, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await bot.get_users(get_user)
    except PeerIdInvalid:
        await message.edit("I don't know that User.")
        await asyncio.sleep(2)
        await message.delete()
        return

    user_details = await bot.get_chat(get_user)
    bio = user_details.bio
    user_pic = await bot.get_profile_photos(user.id)
    pic_count = await bot.get_profile_photos_count(user.id)
    common = await GetCommon(bot, user.id)

    if not user.photo:
        await message.edit(
            WHOIS.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                common_groups=len(common.chats),
                bio=bio if bio else "`No bio set up.`",
            ),
            disable_web_page_preview=True,
        )
    elif user.photo:
        await bot.send_photo(
            message.chat.id,
            user_pic[0].file_id,
            caption=WHOIS_PIC.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                profile_pics=pic_count,
                common_groups=len(common.chats),
                bio=bio if bio else "`No bio set up.`",
                profile_pic_update=ProfilePicUpdate(user_pic),
            ),
            reply_to_message_id=ReplyCheck(message),
        )

        await message.delete()
