import logging
from os import remove
from lexica import Client as lexi
from telegraph import upload_file
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter
from AlinaXIQ import app
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.utils.errors import capture_err
from config import adminlist

def check_nsfw(image_url: str) -> dict:
    client = lexi()
    response = client.AntiNsfw(image_url)
    return response["content"]["sfw"]


@app.on_message(
    ~filters.service & ~filters.private & ~filters.channel & filters.photo, group=6
)
@capture_err
async def nsfw(_, message: Message):
    admins = app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    )
    admins_list = [admin.user.id async for admin in admins]

    if message.from_user.id in admins_list or message.from_user.id in SUDOERS:
        return

    photo = await app.download_media(message.photo.file_id)
    uploaded_file = upload_file(photo)[0]
    url = "https://telegra.ph" + uploaded_file
    try:
        nsfw = check_nsfw(url)
        if nsfw == True:
            await message.reply_text("Safe file, no NSFW content detected")
        else:
            await message.reply_text("NSFW content detected")
        remove(photo)
    except Exception as e:
        remove(photo)
        logging.exception(e)
