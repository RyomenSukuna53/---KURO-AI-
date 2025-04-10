from KuroAI import KuroAI as bot
from KuroAI.KUROMAIN.DATABASE import completed_col
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from config import SUDO_USERS
from KuroAI import HANDLERS

# Command to notify the user that their order is marked as completed
@bot.on_message(filters.command("completed", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def order_completed(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Invalid syntax\nUsage: `/completed <user_id>`", parse_mode=ParseMode.MARKDOWN)
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ Invalid user ID.", parse_mode=ParseMode.MARKDOWN)
        return

    order = completed_col.find_one({"_id": user_id, "status": "approved"})
    if not order:
        await message.reply_text("❌ Order not found or not approved.")
        return

    await bot.send_message(
        chat_id=user_id,
        text="✅ Your bot order has been **marked as completed!**\nWe'll reach out if anything else is needed.",
        parse_mode=ParseMode.MARKDOWN
    )

    await message.reply_text("✅ User has been notified about the order completion.")

# Command to list all completed (approved) orders
@bot.on_message(filters.command("allorders", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def list_all_orders(_, message: Message):
    orders = completed_col.find({"status": "approved"})
    text = "**✅ Approved Orders:**\n\n"

    count = 0
    async for order in orders:
        count += 1
        text += f"**{count}.** Order ID: `{order.get('order_id', 'N/A')}` | User ID: `{order['_id']}` | Name: `{order.get('order_name', 'Unknown')}`\n"

    if count == 0:
        await message.reply_text("No approved orders found.")
    else:
        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


