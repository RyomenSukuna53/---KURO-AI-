from KuroAI import KuroAI as bot
from KuroAI.KUROMAIN.DATABASE import auth_col
from pyrogram import filters
from config import OWNER_ID 
from KuroAI import HANDLERS
from pyrogram.enums import ParseMode
import asyncio

@bot.on_message(filters.command(["unauthorize", "unauth"], prefixes=HANDLERS) & filters.user(OWNER_ID), group=5)
async def unauthorize_user(client, message):
    if not message.reply_to_message:
        return await message.reply(
            "**⚠️ Please reply to a user’s message to unauthorize them.**",
            quote=True
        )

    user = message.reply_to_message.from_user
    user_id = user.id

    is_auth = await auth_col.find_one({"_id": user_id})
    if not is_auth:
        return await message.reply(
            f"❌ **User `{user_id}` is not authorized.**",
            quote=True
        )

    progress_bars = [
        "▱▱▱▱▱▱▱▱▱▱ 0%",
        "▰▱▱▱▱▱▱▱▱▱ 10%",
        "▰▰▱▱▱▱▱▱▱▱ 20%",
        "▰▰▰▱▱▱▱▱▱▱ 30%",
        "▰▰▰▰▱▱▱▱▱▱ 40%",
        "▰▰▰▰▰▱▱▱▱▱ 50%",
        "▰▰▰▰▰▰▱▱▱▱ 60%",
        "▰▰▰▰▰▰▰▱▱▱ 70%",
        "▰▰▰▰▰▰▰▰▱▱ 80%",
        "▰▰▰▰▰▰▰▰▰▱ 90%",
        "▰▰▰▰▰▰▰▰▰▰ 100%"
    ]

    msg = await message.reply_text(
        f"```ini\n[𝗞𝗨𝗥𝗢 𝗔𝗜]\n• Action: Unauthorizing User\n• Target: {user.first_name} [{user_id}]\n• Progress: {progress_bars[0]}```",
        parse_mode=ParseMode.MARKDOWN
    )

    for bar in progress_bars[1:]:
        await asyncio.sleep(0.7)
        await msg.edit_text(
            f"```ini\n[𝗞𝗨𝗥𝗢 𝗔𝗜]\n• Action: Unauthorizing User\n• Target: {user.first_name} [{user_id}]\n• Progress: {bar}```",
            parse_mode=ParseMode.MARKDOWN
        )

    await auth_col.delete_one({"_id": user_id})

    await msg.edit_text(
        f"```ini\n[𝗞𝗨𝗥𝗢 𝗔𝗜]\n• User: {user.first_name} [{user_id}]\n• Status: ✅ Successfully UnAuthorized\n• Progress: {progress_bars[-1]}```",
        parse_mode=ParseMode.MARKDOWN
    )
