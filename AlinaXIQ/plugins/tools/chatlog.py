import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
from config import LOGGER_ID, GROUP_BOT
from AlinaXIQ import app
from AlinaXIQ.utils.database import get_assistant
from AlinaXIQ.utils.database import delete_served_chat


photo = [
"https://graph.org/file/9340f44e4a181b18ac663.jpg",
"https://graph.org/file/50037e072302b4eff55ba.jpg",
"https://graph.org/file/39f39cf6c6c68170f6bf2.jpg",
"https://graph.org/file/abf9931642773bc27ad7f.jpg",
"https://graph.org/file/60764ec9d2b1fda50c2d1.jpg",
"https://graph.org/file/a90c116b776c90d58f5e8.jpg",
"https://graph.org/file/b2822e1b60e62caa43ceb.jpg",
"https://graph.org/file/84998ca9871e231df0897.jpg",
"https://graph.org/file/6c5493fd2f6c403486450.jpg",
"https://graph.org/file/9dd91a4a794f15e5dadb3.jpg",
"https://graph.org/file/0a2fb6e502f6c9b6a04ac.jpg",
"https://graph.org/file/774380facd73524f27d26.jpg"
]


@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = await app.export_chat_invite_link(message.chat.id)
    for members in message.new_chat_members:
        if members.id == app.id:
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"**📝 بۆتی گۆرانی زیادکرا بۆ گرووپ\n\n**"
                f"**____________________________________\n\n**"
                f"**📌 ناوی گرووپ: {message.chat.title}\n**"
                f"**🍂 ئایدی گرووپ: {message.chat.id}\n**"
                f"**🔐 یوزەری گرووپ: @{message.chat.username}\n**"
                f"**🛰 بەستەری گرووپ: [گرووپ]({link})\n**"
                f"**📈 ژمارەی ئەندام: {count}\n**"
                f"**🍓 زیادکرا لەلایەن: {message.from_user.mention}**"
            )
            await app.send_photo(LOGGER_ID, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🍓 بینینی گرووپ 🍓", url=f"{link}")]
         ]))




@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == (await app.get_me()).id:
            remove_by = (
                message.from_user.mention if message.from_user else "**بەکارهێنەری نەناسراو**"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "**گرووپی تایبەت**"
            )
            chat_id = message.chat.id
            left = f"**✫ لێفتی گرووپ ✫\n\nناوی گرووپ : {title}**\n\n**ئایدی گرووپ :** `{chat_id}`\n\n**دەرکرا لەلایەن : {remove_by}\n\nبۆت : @{app.username} **"
            await app.send_photo(GROUP_BOT, photo=random.choice(photo), caption=left, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"نوێکارییەکانی ئەلینا 🍻", url=f"https://t.me/MGIMT")]]))
            await delete_served_chat(chat_id)
    except Exception as e:
        return
