from KuroAI import KuroAI as bot
from KuroAI.KUROMAIN.DATABASE import completed_col
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from config import SUDO_USERS
from KuroAI import HANDLERS


@bot.on_message(filters.command("completed", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def order_completed(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**❌ Invalid Syntax!**\nUsage: `/completed <user_id>`",
            parse_mode=ParseMode.MARKDOWN
        )

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ User ID must be a number.", parse_mode=ParseMode.MARKDOWN)

    order = await completed_col.find_one({"_id": user_id, "status": "approved"})
    if not order:
        return await message.reply_text("❌ No approved order found for this user.")

    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "🎉 **Order Completed!**\n\n"
                "✅ Your bot request has been marked as **completed**.\n"
                "Thank you for trusting us. If you have any questions, feel free to reach out!"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        return await message.reply_text(f"⚠️ Failed to notify the user.\n**Reason:** `{e}`", parse_mode=ParseMode.MARKDOWN)

    await completed_col.delete_one({"_id": user_id})

    await message.reply_text("✅ User has been successfully notified and the order record removed.")
    print(f"✅ Order completed and removed for user_id: {user_id}")


@bot.on_message(filters.command("all_orders", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def all_orders(_, message: Message):
    all_approved = completed_col.find({"status": "approved"})
    text = "📦 **Approved Bot Orders**\n\n"
    count = 0

    async for order in all_approved:
        count += 1
        text += (
            f"**#{count}**\n"
            f"🔹 **Order ID:** `{order.get('order_id')}`\n"
            f"🤖 **Bot Name:** `{order.get('bot_name')}`\n"
            f"📦 **Type:** `{order.get('bot_type')}`\n"
            f"💸 **Budget:** ₹{order.get('budget')}\n"
            f"📝 **Extras:** `{order.get('extra')}`\n"
            f"👤 **User ID:** `{order.get('_id')}`\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        )

    if count == 0:
        await message.reply_text("📭 No approved orders found.")
    else:
        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
