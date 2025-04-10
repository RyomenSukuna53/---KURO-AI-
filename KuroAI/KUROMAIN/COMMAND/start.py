from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from KuroAI import KuroAI as bot
from KuroAI.KUROMAIN.HELPERS.auth import *
import asyncio
import random
from config import * 
from KuroAI import HANDLERS
from config import SUDO_USERS
from KuroAI.KUROMAIN import DATABASE



@bot.on_message(filters.command("start", prefixes=HANDLERS))
async def start_command(client, message):
    user = message.from_user
    user_id = user.id
    bars = [
        "0%   [●◌◌◌◌◌◌◌◌◌]", "10%  [●◌◌◌◌◌◌◌◌◌]", "20%  [●●◌◌◌◌◌◌◌◌]",
        "30%  [●●●◌◌◌◌◌◌◌]", "40%  [●●●●◌◌◌◌◌◌]", "50%  [●●●●●◌◌◌◌◌]",
        "60%  [●●●●●●◌◌◌◌]", "70%  [●●●●●●●◌◌◌]", "80%  [●●●●●●●●◌◌]",
        "90%  [●●●●●●●●●◌]", "100% [●●●●●●●●●●]"
    ]
    MBs = random.randint(5, 100)

    if user_id == OWNER_ID:
        return await message.reply("WELCOME MASTER 👑 You don't need any authorization.")
    
    if user_id in SUDO_USERS:
        return await message.reply(f"WELCOME [{user.first_name}](tg://user?id={user_id}) - Admin access granted.")

    if not auth_col.find_one({"_id": user_id}):
        return await message.reply(
            "**Authorization Required**\n\nPlease join both group and channel then try again.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʝσιи ¢нαηηєℓ", url=f"https://t.me/{SUPPORT_CHANNEL}")],
                [InlineKeyboardButton("ʝσιи gяσυρ", url=f"https://t.me/{SUPPORT_CHAT}")]
            ])
        )

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

    await msg.edit_text(
        f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Initialized✅\n{bars[-1]}\n\nWelcome, {user.first_name}!```",
        parse_mode=ParseMode.MARKDOWN
    )
    await users.insert_one({"_id":user_id}) 
    
