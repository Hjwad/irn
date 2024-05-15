from pyrogram import Client, filters
import requests
import random
import os
import re
import asyncio
import time
from AlinaXIQ import app
from AlinaXIQ.utils.database import add_served_chat_clone, delete_served_chat_clone
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from AlinaXIQ.utils.database import get_assistant
import asyncio
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.mongo.afkdb import LOGGERS as OWNERS
from AlinaXIQ.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from AlinaXIQ import app
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from AlinaXIQ import app
from AlinaXIQ.utils.alina_ban import admin_filter
from AlinaXIQ.utils.decorators.userbotjoin import UserbotWrapper
from AlinaXIQ.utils.database import get_assistant, is_active_chat


@Client.on_message(filters.command(["hi", "hii", "hello", "hui", "good", "gm", "ok", "bye", "welcome", "thanks"] ,prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.group)
async def bot_check(_, message):
    chat_id = message.chat.id
    await add_served_chat_clone(chat_id)


# --------------------------------------------------------------------------------- #




import asyncio
import time

@Client.on_message(filters.command(["/addbots", "زیادکردنی بۆت", "/addbot"],"") & filters.user(int(OWNERS)))
async def add_all(client, message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        await message.reply("**🧑🏻‍💻┋ فەرمانت هەڵە بەکار‌هێنا بەم شێوازە بنووسە :\n/addbots @bot_username**")
        return
    
    bot_username = command_parts[1]
    try:
        userbot = await get_assistant(message.chat.id)
        bot = await client.get_users(bot_username)
        app_id = bot.id
        done = 0
        failed = 0
        lol = await message.reply("**✅┋ زیادکردنی بۆت لە هەموو گرووپەکان**")
        
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1002120144597:
                continue
            try:
                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
                await lol.edit(
                    f"**✅┋ زیادکردنی {bot_username} بۆ گرووپ\n\n✅┋ زیادکرا بۆ: {done} گرووپ\n❌┋ شکستی هێنا لە {failed} گرووپ\n\n⎋┋ زیادکرا لەلایەن ⇜ @{userbot.username}**"
                )
            except Exception as e:
                failed += 1
                await lol.edit(
                    f"**✅┋ زیادکردنی {bot_username} بۆ گرووپ\n\n✅┋ زیادکرا بۆ: {done} گرووپ\n❌┋ شکستی هێنا لە {failed} گرووپ\n\n⎋┋ زیادکرا لەلایەن ⇜ @{userbot.username}**"
                )
            await asyncio.sleep(3)  # Adjust sleep time based on rate limits
        
        await lol.edit(
            f"**🧑🏻‍💻 {bot_username} بە سەرکەوتوویی زیادکرا\n\n✅┋ زیادکرا بۆ: {done} گرووپ\n❌┋ شکستی هێنا لە {failed} گرووپ\n\n⎋┋ زیادکرا لەلایەن ⇜ @{userbot.username}**"
        )
    except Exception as e:
        await message.reply(f"**❌┋ هەڵە : {str(e)}**")
