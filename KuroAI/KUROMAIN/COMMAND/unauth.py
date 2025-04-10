from KuroAI import KuroAI as bot 
from KuroAI.KUROMAIN.DATABASE import auth_col
from pyrogram import Client, filters
from config import *
from KuroAI import HANDLERS
from pyrogram.enums import ParseMode 



@bot.on_message(filters.command(["unauthorize", "unauth"], prefixes=HANDLERS) & filters.user(OWNER_ID), group=5)
async def unauthorize_user(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user's message to unauthorize them.")

    user = message.reply_to_message.from_user
    user_id = user.id

    if not auth_col.find_one({"_id": user_id}):
        return await message.reply("❌ This user is not authorized yet.")

    bars = [
        "0%   [●◌◌◌◌◌◌◌◌◌]", "10%  [●◌◌◌◌◌◌◌◌◌]", "20%  [●●◌◌◌◌◌◌◌◌]",
        "30%  [●●●◌◌◌◌◌◌◌]", "40%  [●●●●◌◌◌◌◌◌]", "50%  [●●●●●◌◌◌◌◌]",
        "60%  [●●●●●●◌◌◌◌]", "70%  [●●●●●●●◌◌◌]", "80%  [●●●●●●●●◌◌]",
        "90%  [●●●●●●●●●◌]", "100% [●●●●●●●●●●]"
    ]

    msg = await message.reply(
        f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Unauthorizing {user_id}...\n{bars[0]}```",
        parse_mode=ParseMode.MARKDOWN
    )

    for bar in bars[1:]:
        await asyncio.sleep(0.2)
        await msg.edit_text(f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> Unauthorizing {user_id}...\n{bar}```", parse_mode=ParseMode.MARKDOWN)

    auth_col.delete_one({"_id": user_id})
    await msg.edit_text(f"```shell\n[𝗞𝗨𝗥𝗢-𝗫𝗔𝗜] ==> {user_id} UnAuthorized✅\n{bars[-1]}```", parse_mode=ParseMode.MARKDOWN)


