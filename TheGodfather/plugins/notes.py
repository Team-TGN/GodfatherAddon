from pyrogram import filters, Client

from TheGodfather import CMD_HELP
from TheGodfather.helpers.pyrohelper import get_arg
import TheGodfather.database.notesdb as db
from config import PREFIX, LOG_CHAT

CMD_HELP.update(
    {
        "Notes": """
『 **Notes** 』
  `save` -> Save a new note. Must be used in reply with one parameter (note name).
  `get` -> Gets the note specified.
  `clear` -> Deletes a note, specified by note name.
  `clearall` -> Deletes all the saved notes.
  `notes` -> List the saved notes.
"""
    }
)

LOG_CHAT = LOG_CHAT


@Client.on_message(filters.command("save", PREFIX) & filters.me)
async def save(app: Client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**You must give a name for a note.**")
        return
    note_name = arg
    note = await db.get_note(note_name)
    if note:
        await message.edit(f"**Note `{note_name}` already exists**")
        return
    reply = message.reply_to_message
    if not reply:
        await message.edit("Reply to a message to save a note")
        return
    copy = await app.copy_message(LOG_CHAT, message.chat.id, reply.message_id)
    await db.save_note(note_name, copy.message_id)
    await message.edit("**Note saved**")


@Client.on_message(filters.command("get", PREFIX) & filters.me)
async def get(app: Client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("Get what?")
        return
    note_name = arg
    note = await db.get_note(note_name)
    if not note:
        await message.edit(f"**Note {note_name} dosen't exists**")
        return
    if message.reply_to_message:
        await app.copy_message(
            message.chat.id,
            LOG_CHAT,
            note,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await app.copy_message(message.chat.id, LOG_CHAT, note)
    await message.delete()


@Client.on_message(filters.command("clear", PREFIX) & filters.me)
async def clear(app: Client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("What do you want to delete?")
        return
    note_name = arg
    note = await db.get_note(note_name)
    if not note:
        await message.edit(f"**Failed to delete note `{note_name}`**")
        return
    await db.rm_note(note_name)
    await message.edit(f"**Succesfully deleted note `{note_name}`**")


@Client.on_message(filters.command("notes", PREFIX) & filters.me)
async def notes(app: Client, message):
    msg = "**Saved Notes**\n\n"
    all_notes = await db.all_notes()
    if not all_notes:
        await message.edit("**No notes has been saved**")
        return
    for notes in all_notes:
        msg += f"◍ `{notes}`\n"
    await message.edit(msg)


@Client.on_message(filters.command("clearall", PREFIX) & filters.me)
async def clearall(app: Client, message):
    await db.rm_all()
    await message.edit("**Removed all saved notes**")
