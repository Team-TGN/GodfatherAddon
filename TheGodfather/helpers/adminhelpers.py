from time import sleep, time

from pyrogram.types import Message
"""Just for multiple clients"""
from pyrogram import Client as app


async def CheckAdmin(message: Message):
    """Check if we are an admin."""
    admin = "administrator"
    creator = "creator"
    ranks = [admin, creator]

    ZAID = await app.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if ZAID.status not in ranks:
        await message.edit("__I'm not Admin!__")
        sleep(2)
        await message.delete()

    else:
        if ZAID.status is not admin or ZAID.can_restrict_members:
            return True
        else:
            await message.edit("__No Permissions to restrict Members__")
            sleep(2)
            await message.delete()
