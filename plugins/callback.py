#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script

from helpers.progress import PRGRS
from helpers.tools import clean_up
from helpers.download import download_file, DATA
from helpers.ffmpeg import extract_audio, extract_subtitle


@trojanz.on_callback_query()
async def cb_handler(client, query):

    if query.data == "start_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("HELP", callback_data="help_data"),
                InlineKeyboardButton("ABOUT", callback_data="about_data")],
            [InlineKeyboardButton("⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/TroJanzHEX")]
        ])

        await query.message.edit_text(
            Script.START_MSG.format(query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "help_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="start_data"),
                InlineKeyboardButton("ABOUT", callback_data="about_data")],
            [InlineKeyboardButton("⭕️ SUPPORT ⭕️", url="https://t.me/TroJanzSupport")]
        ])

        await query.message.edit_text(
            Script.HELP_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "about_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="help_data"),
                InlineKeyboardButton("START", callback_data="start_data")],
            [InlineKeyboardButton("SOURCE CODE", url="https://github.com/TroJanzHEX/Streams-Extractor")]
        ])

        await query.message.edit_text(
            Script.ABOUT_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "download_file":
        await query.answer()
        await query.message.delete()
        await download_file(client, query.message)


    elif query.data == "progress_msg":
        try:
            msg = "Progress Details...\n\nCompleted : {current}\nTotal Size : {total}\nSpeed : {speed}\nProgress : {progress:.2f}%\nETA: {eta}"
            await query.answer(
                msg.format(
                    **PRGRS[f"{query.message.chat.id}_{query.message.message_id}"]
                ),
                show_alert=True
            )
        except:
            await query.answer(
                "Processing your file...",
                show_alert=True
            )


    elif query.data == "close": 
        await query.message.delete()  
        await query.answer(
                "Cancelled...",
                show_alert=True
            ) 


    elif query.data.startswith('audio'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_audio(client, query.message, data)
        except:
            await query.message.edit_text("**Details Not Found**")   


    elif query.data.startswith('subtitle'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_subtitle(client, query.message, data)
        except:
            await query.message.edit_text("**Details Not Found**")  


    elif query.data.startswith('cancel'):
        try:
            query_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)] 
            await clean_up(data['location'])  
            await query.message.edit_text("**Cancelled...**")
            await query.answer(
                "Cancelled...",
                show_alert=True
            ) 
        except:
            await query.answer() 
            await query.message.edit_text("**Details Not Found**")        
