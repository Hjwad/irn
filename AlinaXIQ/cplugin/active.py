from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from unidecode import unidecode

from AlinaXIQ import app
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)


@Client.on_message(filters.command(["/ac","/av","چالاکی پەخش"]),"")
async def start(client: Client, message: Message):
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    await message.reply_text(
        f"<b>✫ زانیاری چالاکی پەخشکردن :</b>\n\n<b>دەنگی : {ac_audio}\nڤیدیۆ : {ac_video}</b>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✯ داخستن ✯", callback_data=f"close")]]
        ),
    )
