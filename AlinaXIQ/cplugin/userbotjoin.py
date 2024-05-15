import asyncio
from AlinaXIQ.misc import SUDOERS
from AlinaXIQ.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
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
from AlinaXIQ.utils.alina_ban import admin_filter
from AlinaXIQ.utils.decorators.userbotjoin import UserbotWrapper
from AlinaXIQ.utils.database import get_assistant, is_active_chat

links = {}


@Client.on_message(
    filters.group & filters.command(["userbotjoin", "userbotjoin", "زیادکردنی یاریدەدەر"], prefixes=["/", "!", "%", "", ".", "@", "#"]) & ~filters.private
)
async def join_group(client, message):

    a = await client.get_me()
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)
    userbot_id = userbot.id
    done = await message.reply("**✅┋ تکایە کەمێك چاوەڕێ بکە بانگھێشت دەکرێت . .**")
    await asyncio.sleep(1)
    # Get chat member object
    chat_member = await client.get_chat_member(chat_id, a.id)

    # Condition 1: Group username is present, bot is not admin
    if (
        message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅┋ بە سەرکەوتوویی یاریدەدەری بۆت جۆینی کرد**")
        except Exception as e:
            await done.edit_text("**🧑🏻‍💻┋ پێویستە ئەدمین بم و ڕۆڵم هەبێت بۆ لادانی باندی یاریدەدەرەکەم**")

    # Condition 2: Group username is present, bot is admin, and Userbot is not banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done.edit_text("**✅┋ بە سەرکەوتوویی یاریدەدەری بۆت جۆینی کرد**")
        except Exception as e:
            await done.edit_text(str(e))

    # Condition 3: Group username is not present/group is private, bot is admin and Userbot is banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await client.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await client.unban_chat_member(chat_id, userbot.id)
                await done.edit_text("**✅┋ باندی یاریدەدەر لادەدرێت . .**")
                await userbot.join_chat(message.chat.username)
                await done.edit_text(
                    "**👾┋ ئەکاونتی یاریدەدەر باندکراوە، بەڵام ئێستا باندی لادەدەم، دواتر جۆینی گرووپ دەکات ✅**"
                )
            except Exception as e:
                await done.edit_text(
                    "**❌┋ شکستی هێنا لە جۆین کردن، تکایە ڕۆڵی باند و بانگھێشت کردنم پێبدە تاوەکو بتوانم ڕاستەوخۆ زیادی بکەمە گرووپ دووبارە بنووسە : /userbotjoin **"
                )
        return

    # Condition 4: Group username is not present/group is private, bot is not admin
    if (
        not message.chat.username
        and not chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        await done.edit_text("**🧑🏻‍💻┋ پێویستە ئەدمین بم بۆ بانگھێشت کردنی یاریدەدەرەکەم**")

    # Condition 5: Group username is not present/group is private, bot is admin
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        try:
            try:
                userbot_member = await client.get_chat_member(chat_id, userbot.id)
                if userbot_member.status not in [
                    ChatMemberStatus.BANNED,
                    ChatMemberStatus.RESTRICTED,
                ]:
                    await done.edit_text("**✅┋ ئەکاونتی یاریدەدەر پێشتر جۆینی کردووە و لە گرووپە**")
                    return
            except Exception as e:
                await done.edit_text("**✅┋ تکایە کەمێك چاوەڕێ بکە بانگھێشت دەکرێت . .**")
                await done.edit_text("**✅┋ تکایە کەمێك چاوەڕێ بکە بانگھێشت دەکرێت . .**")
                invite_link = await client.create_chat_invite_link(
                    chat_id, expire_date=None
                )
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text("**✅┋ بە سەرکەوتوویی یاریدەدەری بۆت جۆینی کرد**")
        except Exception as e:
            await done.edit_text(
                f"**💀┋➻ من یاریدەدەرەکەم دۆزیەوە و وە جۆینی گرووپی نەکردووە بەڵام من ڕۆڵی بانگھێشت کردنی خەڵکیم نییە بۆیە دەبێت ڕۆڵی بانگھێشت کردنم پێبدەیت دواتر دووبارە بنووسیت : /userbotjoin \n\n➥ ئایدی » @{userbot.username} **"
            )

    # Condition 6: Group username is not present/group is private, bot is admin and Userbot is banned
    if (
        not message.chat.username
        and chat_member.status == ChatMemberStatus.ADMINISTRATOR
    ):
        userbot_member = await client.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [
            ChatMemberStatus.BANNED,
            ChatMemberStatus.RESTRICTED,
        ]:
            try:
                await client.unban_chat_member(chat_id, userbot.id)
                await done.edit_text(
                    "**✅┋ ئەکاونتی یاریدەدەر باندی لادرا\nدووبارە بنووسە : /userbotjoin**"
                )
                invite_link = await client.create_chat_invite_link(
                    chat_id, expire_date=None
                )
                await asyncio.sleep(2)
                await userbot.join_chat(invite_link.invite_link)
                await done.edit_text(
                    "**👾┋ ئەکاونتی یاریدەدەر باندکراوە، بەڵام ئێستا باندی لادەدەم، دواتر جۆینی گرووپ دەکات ✅**"
                )
            except Exception as e:
                await done.edit_text(
                    f"**✅┋➻  من یاریدەدەرەکەم دۆزیەوە و وە باندکراوە لە گرووپ بەڵام من ڕۆڵی لادانی باندم نییە بۆیە دەبێت ڕۆڵی باند کردنم پێبدەیت دواتر دووبارە بنووسیت : /userbotjoin \n\n➥ ئایدی » @{userbot.username} **"
                )
        return


@Client.on_message(filters.command(["/userbotleave", "دەرکردنی یاریدەدەر", "/assleft"], prefixes=["/", "!", "%", "", ".", "@", "#"]) & filters.group & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await client.send_message(
            message.chat.id, "**✅┋ بە سەرکەوتوویی ئەکاونتی یاریدەدەر لێفتی کرد**"
        )
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["leaveall","لێفتی گشتی"],"") & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("**✅┋ ئەکاونتی یاریدەدەری بۆت لێفت دەکات لە هەموو گرووپەکان**")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1001962701094:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"**✅┋ لێفت دەکات لە هەموو گرووپەکان . .\n\n✅┋ لێفت دەکات : {left} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**"
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"**✅┋ لێفت دەکات . .\n\n✅┋ لێفتی کرد لە : {left} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**"
                )
            await asyncio.sleep(3)
    finally:
        await client.send_message(
            message.chat.id,
            f"**✅┋ لێفتی کرد لە : {left} گرووپ\n❌┋ شکستی هێنا لە : {failed} گرووپ**",
        )
