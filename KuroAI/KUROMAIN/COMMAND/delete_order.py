from KuroAI import KuroAI
from KuroAI.KUROMAIN.DATABASE import auth_col, completed_col
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

@KuroAI.on_message(filters.command("del_order", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def delete_orders(client, message):
    if len(message.command) < 2:
        await message.reply_text("SAX 🎷🎷🎷\n⚠️ GIVE ORDER ID ALSO")
        return

    order_id = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason given"

    real_order = await completed_col.find_one({"order_id": order_id})
    if not real_order:
        await message.reply_text("SAX 🎷🎷🎷\n❌ THIS ORDER ID NOT IN OUR COLLECTION SIR")
        return

    await completed_col.delete_one({"order_id": order_id})
    await message.reply_text(f"✅ ORDER `{order_id}` DELETED SUCCESSFULLY!\nReason: {reason}")


@KuroAI.on_message(filters.command("del_all_orders", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def delete_all_orders(client, message):
    confirm_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirm Delete", callback_data="confirm_del_all_orders")]
    ])
    await message.reply("⚠️ Are you sure you want to delete **ALL completed orders**?", reply_markup=confirm_button)

@KuroAI.on_callback_query(filters.regex("confirm_del_all_orders"))
async def confirm_delete_all_orders(client, callback_query):
    await completed_col.delete_many({})
    await callback_query.message.edit_text("✅ All orders deleted successfully from `completed_col`.")




