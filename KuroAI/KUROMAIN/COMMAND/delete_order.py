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

    order = await completed_col.find_one({"order_id": order_id})
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


@KuroAI.on_message(filters.command("del_all_orders", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def prompt_delete_all_orders(_, message: Message):
    confirm_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirm Deletion", callback_data="confirm_del_all_orders")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_del_all_orders")]
    ])
    await message.reply(
        "**⚠️ Confirm Bulk Deletion**\n\n"
        "You're about to **permanently delete all completed orders**.\n"
        "This action is irreversible. Are you sure?",
        reply_markup=confirm_markup,
        parse_mode=ParseMode.MARKDOWN
    )


@KuroAI.on_callback_query(filters.regex("confirm_del_all_orders"))
async def confirm_delete_all_orders(_, callback_query: CallbackQuery):
    await completed_col.delete_many({})
    await callback_query.message.edit_text(
        "✅ **All completed orders have been permanently deleted.**",
        parse_mode=ParseMode.MARKDOWN
    )


@KuroAI.on_callback_query(filters.regex("cancel_del_all_orders"))
async def cancel_delete_all_orders(_, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "❌ **Bulk deletion cancelled.**\n\nNo orders were deleted.",
        parse_mode=ParseMode.MARKDOWN
    )
