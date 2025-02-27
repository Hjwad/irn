from pyrogram import filters, Client
from pyrogram.types import Message

from AlinaXIQ import app
from AlinaXIQ.core.call import Alina
from AlinaXIQ.utils.database import set_loop
from AlinaXIQ.utils.decorators import AdminRightsCheck
from AlinaXIQ.utils.inline import close_markup
from config import BANNED_USERS


@Client.on_message(
    filters.command(
        ["end", "stop", "cend", "cstop","ڕاگرتن","وەستان"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & ~filters.private
    & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await Alina.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    user_mention = message.from_user.mention if message.from_user else "𝖠𝖽𝗆𝗂𝗇"
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
