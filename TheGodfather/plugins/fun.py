import asyncio
from collections import deque
from random import randint

from pyrogram import filters, Client
from pyrogram.types import Message
from config import PREFIX


emojis = {
    "moon": list("ππππππππ"),
    "clock": list("πππππππππππ"),
    "thunder": list("βοΈπ€οΈβπ₯οΈβοΈπ©οΈπ§οΈβοΈβ‘π©οΈπ§οΈπ¦οΈπ₯οΈβπ€οΈβοΈ"),
    "earth": list("ππππππππ"),
    "heart": list("β€οΈπ§‘πππππ€"),
}
emoji_commands = [x for x in emojis]


@Client.on_message(filters.command(emoji_commands, PREFIX) & filters.me)
async def emoji_cycle(bot: Client, message: Message):
    deq = deque(emojis[message.command[0]])
    try:
        for _ in range(randint(16, 32)):
            await asyncio.sleep(0.3)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except Exception:
        await message.delete()


special_emojis_dict = {
    "target": {"emoji": "π―", "help": "The special target emoji"},
    "dice": {"emoji": "π²", "help": "The special dice emoji"},
    "bb": {"emoji": "π", "help": "The special basketball emoji"},
    "soccer": {"emoji": "β½οΈ", "help": "The special football emoji"},
}
special_emoji_commands = [x for x in special_emojis_dict]


@Client.on_message(filters.command(special_emoji_commands, PREFIX) & filters.me)
async def special_emojis(bot: Client, message: Message):
    emoji = special_emojis_dict[message.command[0]]
    await message.delete()
    await bot.send_dice(message.chat.id, emoji["emoji"])

__MODULE__ = "Fun"
__HELP__ = f"""
**π This module just for fun/ Animation.**
`.moon` - **Moon animation**
`.clock` - **Clock Animation**
`.thunder` - **Thunderβ‘ Animation**
`.earth` - **Earth Animation**
`.heart` - **Heart Animation**
"""


