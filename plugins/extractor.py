import os
import pyrogram

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import Script
from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

file_types = [
    "video/x-msvideo",
    "video/x-flv",
    "video/webm",
    "video/x-m4v",
    "video/mp4",
    "video/mpeg",
    "video/ogg",
    "video/x-matroska",
    "video/webm"
]


@trojanz.on_message(filters.private & (filters.document | filters.video))
async def confirm_dwnld(client, message):
    media = message
    filetype = media.document or media.video

    if int(filetype.file_size/1024/1024) <= 8:

        if filetype.mime_type in file_types:
            await message.reply_text(
                "**Select the Optins Below**",
                quote=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="DOWNLOAD", callback_data="download_file")],
                    [InlineKeyboardButton(text="CANCEL", callback_data="close")]]
                )
            )
        else:
            await message.reply_text(
                "```Invalid Media```",
                quote=True
            )
    else:
        await message.reply_text(
            "**Cheriya Size Ayakkadey...**",
            quote=True
        )

