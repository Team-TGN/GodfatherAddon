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

@bot.on_message(filters.command(["help"]))
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await message.reply_text(text, reply_markup=keyboard)




async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """**Welcome to Godfather help Menu :
Click On The Button Below ✨...**
""".format(
            first_name=name
        ),
        keyboard,
    )
home_text_pm = "Hey!"

@bot.on_callback_query(filters.regex("close"))
async def close(_, CallbackQuery):
    await CallbackQuery.message.delete()

@bot.on_callback_query(filters.regex("gfs"))
async def godfather(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""**Welcome to Godfather help Menu :
Click On The Button Below ✨...**
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "**📂 Welcome to help Menu of :** ", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📂 Back", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="📂 Close", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await bot.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
