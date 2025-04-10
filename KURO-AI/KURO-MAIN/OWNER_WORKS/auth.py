from pyrogram import filters
from pyrogram.enums import ParseMode
from KuroAI import KuroAI as bot
from KuroAI.KURO-MAIN.HELPERS.auth import *
import asyncio
from config import *



@bot.on_message(filters.command(["authorize", "auth"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def authorize_user(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user's message to authorize them.")
    
    user_id = message.reply_to_message.from_user.id
    bars = [
        "0%   [●◌◌◌◌◌◌◌◌◌]", "10%  [●◌◌◌◌◌◌◌◌◌]", "20%  [●●◌◌◌◌◌◌◌◌]",
        "30%  [●●●◌◌◌◌◌◌◌]", "40%  [●●●●◌◌◌◌◌◌]", "50%  [●●●●●◌◌◌◌◌]",
        "60%  [●●●●●●◌◌◌◌]", "70%  [●●●●●●●◌◌◌]", "80%  [●●●●●●●●◌◌]",
        "90%  [●●●●●●●●●◌]", "100% [●●●●●●●●●●]"
    ]

    msg = await message.reply(
        f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜]==> Authorizing {user_id}...\n{bars[0]}```",
        parse_mode=ParseMode.MARKDOWN
    )

    for bar in bars[1:]:
        await asyncio.sleep(0.2)
        await msg.edit_text(
            f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜]==> Authorizing {user_id}...\n{bar}```",
            parse_mode=ParseMode.MARKDOWN
        )

    authorized_users.add(user_id)
    await msg.edit_text(
        f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜]==> {user_id} Authorized✅\n{bars[-1]}```",
        parse_mode=ParseMode.MARKDOWN
    )

