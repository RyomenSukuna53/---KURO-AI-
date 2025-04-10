from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from KuroAI import KuroAI as bot
from KuroAI.KURO-MAIN.HELPERS.auth import *
import asyncio
import random

@bot.on_message(filters.command("start", prefixes=HANDLER))
async def start_command(client, message):
    user = message.from_user.id
    bars = [
        "0%   [●◌◌◌◌◌◌◌◌◌]", "10%  [●◌◌◌◌◌◌◌◌◌]", "20%  [●●◌◌◌◌◌◌◌◌]",
        "30%  [●●●◌◌◌◌◌◌◌]", "40%  [●●●●◌◌◌◌◌◌]", "50%  [●●●●●◌◌◌◌◌]",
        "60%  [●●●●●●◌◌◌◌]", "70%  [●●●●●●●◌◌◌]", "80%  [●●●●●●●●◌◌]",
        "90%  [●●●●●●●●●◌]", "100% [●●●●●●●●●●]"
    ]
    MBs = random.randint(5, 100)

    if not await check_authorized(client, user):
        await message.reply(
            "**Need Authorization to use this bot.**\n\nJoin both group & channel and try again.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʝσιη ¢нαηηєℓ", url=f"https://t.me/{SUPPORT_CHANNEL}")],
                [InlineKeyboardButton("ʝσιη gяσυρ", url=f"https://t.me/{SUPPORT_CHAT}")]
            ])
        )
        return

    if user not in authorized_users:
        await message.reply("You're not authorized yet. Ask admin to authorize you.")
        return

    msg = await message.reply(
        f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Initializing...\n{bars[0]}\n0 / {MBs} MB```",
        parse_mode=ParseMode.MARKDOWN
    )

    for mb in range(1, MBs + 1):
        await asyncio.sleep(0.2)
        percent = int((mb / MBs) * 100)
        bar_index = min(percent // 10, 10)
        bar = bars[bar_index]
        await msg.edit_text(
            f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Initializing...\n{bar}\n{mb} / {MBs} MB```",
            parse_mode=ParseMode.MARKDOWN
        )

    await msg.edit_text(f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> \"Intialized✅\n{bars[10]}\n\nNOW YOU CAN USE ME MASTER!.\"```", 
                        parse_mode=ParseMode.MARKDOWN) 
    
    
