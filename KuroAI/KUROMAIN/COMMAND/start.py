from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from KuroAI import KuroAI as bot
import asyncio
import random
from config import * 
from KuroAI import HANDLERS
from config import SUDO_USERS
from KuroAI.KUROMAIN.DATABASE import *



@bot.on_message(filters.command("start", prefixes=HANDLERS), group=5)
async def start_command(client, message):
    user = message.from_user
    user_id = user.id
    bars = [
        "0%   [●◌◌◌◌◌◌◌◌◌]", "10%  [●◌◌◌◌◌◌◌◌◌]", "20%  [●●◌◌◌◌◌◌◌◌]",
        "30%  [●●●◌◌◌◌◌◌◌]", "40%  [●●●●◌◌◌◌◌◌]", "50%  [●●●●●◌◌◌◌◌]",
        "60%  [●●●●●●◌◌◌◌]", "70%  [●●●●●●●◌◌◌]", "80%  [●●●●●●●●◌◌]",
        "90%  [●●●●●●●●●◌]", "100% [●●●●●●●●●●]"
    ]
    

    if not auth_col.find_one({"_id": user_id}):
        return await message.reply(
            "**Authorization Required**\n\nPlease join both group and channel then try again.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʝσιи ¢нαηηєℓ", url=f"https://t.me/{SUPPORT_CHANNEL}")],
                [InlineKeyboardButton("ʝσιи gяσυρ", url=f"https://t.me/{SUPPORT_CHAT}")]
            ])
        )

    else:
        start_msg = ">✨ 𝙲𝙾𝙳𝙴𝚂 𝙾𝙵 𝗟𝗘𝗚𝗘𝗡𝗗𝗦 | 伝説 ✨\n\n"  
        f"Welcome To The  𝙲𝙾𝙳𝙴𝚂 𝙾𝙵 𝗟𝗘𝗚𝗘𝗡𝗗𝗦 | 伝説 [𝙲𝙾𝙻-𝙓•忍者] {message.from_user.first_name}\n\n"
        "Your Smart Order + AI Bot is Here!\n\n"
        "🔹 Use /order – Place your custom order in seconds\n"  
        "🔹 Use /track – Track your order status anytime\n" 
        "🔹 Use /ai – Ask anything, get instant AI-powered replies\n" 
        "🔹 Use /help – Explore all features\n\n"  
        ">⚡ Fast. Smart. Legendary.\n\n"
        ">Made for Legends, by Legends.\n\n"
        ">If you have any query or need guide click the button below❤‍🔥❤‍🔥❤‍🔥"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("gυι∂є📕", url="https://t.me/RaijinCodes_Ultra")]
    ]) 
        
        await message.reply_text(start_msg, reply_markup=keyboard) 
