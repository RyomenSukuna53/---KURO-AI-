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

    order = await completed_col.find_one({"_id": user_id, "status": "approved"})
    if not order:
        await message.reply_text("❌ Order not found or not approved.")
        return

    await bot.send_message(
        chat_id=user_id,
        text="✅ Your bot order has been **marked as completed!**\nWe'll reach out if anything else is needed.",
        parse_mode=ParseMode.MARKDOWN
    )

    await message.reply_text("✅ User has been notified about the order completion.")
    await completed_col.delete_one({"_id": user_id}) 
    print("work completdd user_id delted") 


# Command to list all completed (approved) orders
@bot.on_message(filters.command("all_orders", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def all_orders(_, message: Message):
    all_approved = completed_col.find({"status": "approved"})
    text = "**✅ Completed Orders:**\n\n"
    count = 0

    async for order in all_approved:
        count += 1
        text += (
            f"**#{count}**\n"
            f"**ID:** {order.get('order_id') }\n"
            f"**Bot Name:** {order.get('bot_name')}\n"
            f"**Type:** {order.get('bot_type')}\n"
            f"**Budget:** ₹{order.get('budget')}\n"
            f"**Extra:** {order.get('extra')}\n"
            "----------------------\n"
        )

    if count == 0:
        await message.reply("No approved orders yet.")
    else:
        await message.reply(text)



