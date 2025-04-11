from KuroAI import KuroAI, HANDLERS
from config import SUDO_USERS
from pyrogram import filters
from pyrogram.enums import ParseMode
from KuroAI.KUROMAIN.DATABASE import auth_col


@KuroAI.on_message(filters.command("msg", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def send_msg_to_user(_, message):
    if len(message.command) < 3:
        return await message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "Correct Format:\n`/msg <user_id> <your_message>`",
            parse_mode=ParseMode.MARKDOWN
        )

    reciever = message.command[1]
    query = " ".join(message.command[2:])

    if not reciever.isdigit():
        return await message.reply_text(
            "⚠️ **User ID must be a number.**\nPlease enter a valid Telegram User ID.",
            parse_mode=ParseMode.MARKDOWN
        )

    if len(reciever) < 8:
        return await message.reply_text(
            "⚠️ **This doesn't look like a valid Telegram User ID.**",
            parse_mode=ParseMode.MARKDOWN
        )

    is_verified = await auth_col.find_one({"_id": int(reciever)})
    if not is_verified:
        return await message.reply_text(
            "❌ **User Not Authorized!**\nThis user is not in the authorized user list.",
            parse_mode=ParseMode.MARKDOWN
        )

    try:
        await KuroAI.send_message(chat_id=int(reciever), text=f"✉️ Message from {message.from_user.first_name}\n{query}")
        await message.reply_text(
            f"✅ **Message sent successfully!**\n\n"
            f"**Recipient:** `{reciever}`\n"
            f"**Message:**\n{query}",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.reply_text(
            f"❌ **Failed to send message!**\n\n"
            f"**Error:** `{e}`",
            parse_mode=ParseMode.MARKDOWN
        )
