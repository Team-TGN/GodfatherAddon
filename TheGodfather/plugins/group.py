import os
from pyrogram import filters, Client

from config import PREFIX


@Client.on_message(filters.command("rename", PREFIX) & filters.me)
def rename(_, message):
    try:
        filename = message.text.replace(message.text.split(" ")[0], "")
    except Exception as e:
        print(e)
    if reply := message.reply_to_message:
        omk = message.reply_text("Downloading.....")
        path = reply.download(file_name=filename)
        omk.edit("Uploading.....")
        message.reply_document(path)
        os.remove(path)
