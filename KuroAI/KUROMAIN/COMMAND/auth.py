from pyrogram import filters
from pyrogram.enums import ParseMode
from KuroAI import KuroAI as bot
from config import *
import asyncio
from KuroAI.KUROMAIN.DATABASE import auth_col
from KuroAI import HANDLERS


@bot.on_message(filters.command(["authorize", "auth"], prefixes=HANDLERS) & filters.user(OWNER_ID))
async def authorize_user(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "❌ Please reply to a user you want to authorize."
        )

    user = message.reply_to_message.from_user
    user_id = user.id

    if await auth_col.find_one({"_id": user_id}):
        return await message.reply_text(
            f"✅ User [{user.first_name}](tg://user?id={user_id}) is already authorized.",
            parse_mode=ParseMode.MARKDOWN
        )

    progress_bars = [
        "0%   [░░░░░░░░░░]", "10%  [█░░░░░░░░░░]", "20%  [██░░░░░░░░░]",
        "30%  [███░░░░░░░]", "40%  [████░░░░░░]", "50%  [█████░░░░░]",
        "60%  [██████░░░░]", "70%  [███████░░░]", "80%  [████████░░]",
        "90%  [█████████░]", "100% [██████████]"
    ]

    msg = await message.reply_text(
        f"```bash\n[𝗞𝗨𝗥𝗢 𝗔𝗜] :: Authorizing User: {user.first_name}\n{progress_bars[0]}```",
        parse_mode=ParseMode.MARKDOWN
    )

    for bar in progress_bars[1:]:
        await asyncio.sleep(0.8)
        await msg.edit_text(
            f"```bash\n[ KURO-AI SYSTEM ] :: Authorizing User: {user.first_name}\n{bar}```",
            parse_mode=ParseMode.MARKDOWN
        )

    await auth_col.insert_one({"_id": user_id})
    await msg.edit_text(
        f"```bash\n[ KURO-AI SYSTEM ] :: ✅ Authorization Complete!\nUser: {user.first_name} ({user_id})\n{progress_bars[-1]}```",
        parse_mode=ParseMode.MARKDOWN
    )

    await message.reply_text(
        f"✨ [{user.first_name}](tg://user?id={user_id}) has been **successfully authorized** into the system!",
        parse_mode=ParseMode.MARKDOWN
    )
