from config import PREFIX

from pyrogram import filters, Client

from TheGodfather.database.gmutedb import get_gmuted_users, gmute_user, ungmute_user
from TheGodfather.helpers.pyrohelper import get_arg
from TheGodfather.helpers.adminhelpers import CheckAdmin


@Client.on_message(filters.command("gmute", PREFIX) & filters.me)
async def gmute(app: Client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Whome should I gmute?**")
            return
    get_user = await app.get_users(user)
    await gmute_user(get_user.id)
    await message.edit(f"**Gmuted {get_user.first_name}, LOL!**")
