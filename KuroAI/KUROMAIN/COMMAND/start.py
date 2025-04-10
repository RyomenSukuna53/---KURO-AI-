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

    msg = await message.reply(f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Initializing...\n{bars[0]}\n```",
        parse_mode=ParseMode.MARKDOWN
    )
    for bar in bars:
        asyncio.sleep(0.7) 
        await msg.edit_text(f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Initializing...\n{bar}\n```",
        parse_mode=ParseMode.MARKDOWN
                           )

    await msg.edit_text(f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Initializing...✅\n{bars[10]}\nωєℓ¢σмє {message.from_user.first_name} тσ συя ∂єѕтʝηу ησω уσυ ¢αη υѕє συя αι αη∂ ¢αη gινє σя∂єяѕ тσ мαкє уσυя вσтѕ тσ. ❤```",
                        parse_mode=ParseMode.MARKDOWN
    )

