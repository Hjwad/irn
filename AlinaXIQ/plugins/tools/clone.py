import re
import logging
import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import (
    AccessTokenExpired,
    AccessTokenInvalid,
)
from AlinaXIQ.utils.database import get_assistant
from config import API_ID, API_HASH
from AlinaXIQ import app
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.utils.database import get_assistant, clonebotdb
from config import LOGGER_ID

CLONES = set()


@app.on_message(filters.command("clone") & SUDOERS)
async def clone_txt(client, message):
    userbot = await get_assistant(message.chat.id)
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("**✅| تکایە کەمێك چاوەڕێ بکە پڕۆسەی دەکەم**")
        try:
            ai = Client(
                bot_token,
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="AlinaXIQ.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            bot_users = await ai.get_users(bot.username)
            bot_id = bot_users.id

        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text(
                "**🤖| تۆ تۆکنێکی هەڵەت پێمداوە تکایە دڵنیابەوە لە تۆکنی بۆت**"
            )
            return
        except Exception as e:
            await mi.edit_text(f"**❌| هەڵە ڕوویدا لە :\n {str(e)} **")
            return

        # Proceed with the cloning process
        await mi.edit_text(
            "**✅| پرۆسەی کۆپی کردن دەستی پێکرد. تکایە چاوەڕێی دەستپێکردنی بۆتەکە بن**"
        )
        try:

            await app.send_message(
                LOGGER_ID, f"**✅| بۆتی نوێ\n\n🤖| بۆت : @{bot.username}**"
            )
            await userbot.send_message(bot.username, "/start")

            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": message.from_user.id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
            }
            clonebotdb.insert_one(details)
            CLONES.add(bot.id)
            await mi.edit_text(
                f"🤖| بۆتی @{bot.username}\n✅| بە سەرکەوتوویی دروستکرا\n❌| دەتوانی بیسڕیتەوە بەم فەرمانە : /delclone**"
            )
        except BaseException as e:
            logging.exception("Error while cloning bot.")
            await mi.edit_text(
                f"⚠️ <b>هەڵە:</b>\n\n<code>{e}</code>\n\n**نامەکە بنێرە ئێرە @IQSUPP بۆ وەرگرتنی ئەکاونتی یاریدەدەر**"
            )
    else:
        await message.reply_text(
            "**تۆکنی بۆت بنووسە لە دوای فەرمانەکە\nنموونە :\n/clone 383993302:HS933NDEO90-E3EDE**"
        )


@app.on_message(
    filters.command(
        [
            "deletecloned",
            "delcloned",
            "delclone",
            "deleteclone",
            "removeclone",
            "cancelclone",
        ]
    )
)
async def delete_cloned_bot(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "**تۆکنی بۆت بنووسە لە دوای فەرمانەکە\nنموونە :\n/delclone 383993302:HS933NDEO90-E3EDE**"
            )
            return

        bot_token = " ".join(message.command[1:])
        await message.reply_text("**🤖| تۆکنی بۆت دەپشکنم **")

        cloned_bot = clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await message.reply_text(
                "**✅| بۆتە کۆپی کراوەکەت لە سێرڤەر دەرکرا و سڕدرایەوە\nبۆ دروستکردنی بۆت : /clone**"
            )
        else:
            await message.reply_text(
                "**❌| ئەم بۆتە لە لیستی بۆتە کۆپی کراوەکان نییە**"
            )
    except Exception as e:
        await message.reply_text("**❌| هەڵە ڕوویدا لە سڕینەوەی بۆت**")
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots........")
        bots = clonebotdb.find()
        async for bot in bots:
            bot_token = bot["token"]
            ai = Client(
                f"{bot_token}",
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="AlinaXIQ.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            if bot.id not in CLONES:
                try:
                    CLONES.add(bot.id)
                except Exception:
                    pass
    except Exception as e:
        logging.exception("Error while restarting bots.")


@app.on_message(filters.command("clones") & SUDOERS)
async def list_cloned_bots(client, message):
    try:
        cloned_bots = clonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)

        if not cloned_bots_list:
            await message.reply_text("**هیچ بۆتێ دروست نەکراوە**")
            return

        total_clones = len(cloned_bots_list)
        text = f"**🤖| کۆی گشتی بۆتەکان : {total_clones}\n\n**"

        for bot in cloned_bots_list:
            text += f"**ئایدی بۆت :** `{bot['bot_id']}`\n"
            text += f"**ناوی بۆت : {bot['name']}\n**"
            text += f"**یوزەری بۆت : @{bot['username']}\n\n**"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("**❌| هەڵە ڕوویدا لە هێنانی لیستی بۆت **")

@app.on_message(filters.command("delallclone") & SUDOERS)
async def delete_all_cloned_bots(client, message):
    try:
        await message.reply_text("**🤖| سڕینەوەی هەموو بۆتە کۆپی کراوەکان**")

        # Delete all cloned bots from the database
        clonebotdb.delete_many({})

        # Clear the CLONES set
        CLONES.clear()

        await message.reply_text("**✅| هەموو بۆتە کۆپی کراوەکان بە سەرکەوتوویی سڕاونەتەوە**")
    except Exception as e:
        await message.reply_text("**❌| هەڵە ڕوویدا لە سڕینەوەی بۆتەکان**")
        logging.exception(e)
