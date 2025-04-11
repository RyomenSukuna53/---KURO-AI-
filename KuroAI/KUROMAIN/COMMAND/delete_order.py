from KuroAI import KuroAI
from KuroAI.KUROMAIN.DATABASE import auth_col, completed_col
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import SUDO_USERS
from KuroAI import HANDLERS


@KuroAI.on_message(filters.command("del_order", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def delete_single_order(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "Use the command like this:\n"
            "`/del_order <order_id> [reason]`\n\n"
            "Example:\n`/del_order 456 Incomplete info provided`",
            parse_mode=ParseMode.MARKDOWN
        )

    order_id = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason specified."

    order = completed_col.find_one({"order_id": order_id})
    if not order:
        return await message.reply_text(
            f"⚠️ **Order ID `{order_id}` not found** in the database.",
            parse_mode=ParseMode.MARKDOWN
        )

    await completed_col.delete_one({"order_id": order_id})

    await message.reply_text(
        f"✅ **Order Deleted Successfully!**\n\n"
        f"🆔 **Order ID:** `{order_id}`\n"
        f"🗑️ **Deleted By:** `{message.from_user.id}`\n"
        f"📄 **Reason:** {reason}",
        parse_mode=ParseMode.MARKDOWN
    )


