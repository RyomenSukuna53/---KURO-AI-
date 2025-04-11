from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from KuroAI import KuroAI as bot
from config import OWNER_ID, SUDO_USERS
from KuroAI.KUROMAIN.DATABASE import order_col, pending_col, completed_col, auth_col
from KuroAI import HANDLERS
import random
from pyrogram.enums import ParseMode

user_states = {}

@bot.on_message(filters.command("order", prefixes=HANDLERS) & filters.private)
async def start_order(_, message: Message):
    user_id = message.from_user.id
    auth_user = await auth_col.find_one({"_id": user_id})
    pending = await completed_col.find_one({"_id": user_id})

    if not auth_user:
        await message.reply_text("⛔ Access Denied!\n\nOnly authorized users can place an order.")
        return

    if pending:
        await message.reply_text("⚠️ One Order at a Time!\n\nYou already have a pending order. Wait until it's completed.")
        return

    user_states[user_id] = {"step": "name", "user_id": user_id}
    await message.reply("📦 Let's Build Your Bot!\n\nEnter your **Bot Name** to get started:")

@bot.on_message(filters.text & filters.private & ~filters.command(["order"], prefixes=HANDLERS))
async def handle_order_step(_, message: Message):
    user_id = message.from_user.id
    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state["step"] == "name":
        state["bot_name"] = message.text
        state["step"] = "type"
        await message.reply("🤖 What type of bot is this?\n\n(Example: Music, Game, AI)")

    elif state["step"] == "type":
        state["bot_type"] = message.text
        state["step"] = "function"
        await message.reply("⚙️ What is the core purpose of your bot?")

    elif state["step"] == "function":
        state["bot_function"] = message.text
        state["step"] = "commands"
        await message.reply("🧩 List the commands you'd like in your bot.\n\n(You can send comma-separated commands or a list.)")

    elif state["step"] == "commands":
        state["bot_commands"] = message.text
        state["step"] = "budget"
        await message.reply("💰 What’s your budget? (in ₹)")

    elif state["step"] == "budget":
        try:
            budget = int(message.text)
            if budget < 100:
                await message.reply("❌ Minimum budget is ₹100.\n\nPlease enter a higher amount.")
                return
            state["budget"] = budget
            state["step"] = "extra"
            await message.reply("✉️ Any extra information you'd like to add?\n\nSend `/skip` to skip this step.")
        except ValueError:
            await message.reply("⚠️ Please enter a **valid number** for the budget.")
            return

    elif state["step"] == "extra":
        state["extra"] = message.text if message.text != "/skip" else "None"
        state["step"] = "confirm"

        text = (
            f"✅ **Confirm Your Order**\n\n"
            f"• **Bot Name:** `{state['bot_name']}`\n"
            f"• **Type:** `{state['bot_type']}`\n"
            f"• **Function:** `{state['bot_function']}`\n"
            f"• **Commands:** `{state['bot_commands']}`\n"
            f"• **Budget:** ₹{state['budget']}\n"
            f"• **Extra:** `{state['extra']}`\n\n"
            f"Reply with `confirm` to place your order or `cancel` to discard it."
        )
        await message.reply(text, parse_mode=ParseMode.MARKDOWN)

    elif state["step"] == "confirm":
        if message.text.lower() == "confirm":
            order_data = {
                "user_id": user_id,
                "username": message.from_user.username,
                "bot_name": state['bot_name'],
                "bot_type": state['bot_type'],
                "bot_function": state['bot_function'],
                "bot_commands": state['bot_commands'],
                "budget": state['budget'],
                "extra": state['extra'],
                "status": "pending"
            }

            await order_col.insert_one(order_data)
            await pending_col.insert_one(order_data)

            await message.reply("✅ Your order has been submitted for admin review!")

            await bot.send_message(
                OWNER_ID,
                f"📩 **New Bot Order Received**\n\n"
                f"👤 **User:** [{message.from_user.first_name}](tg://user?id={user_id})\n"
                f"• **Bot Name:** `{state['bot_name']}`\n"
                f"• **Type:** `{state['bot_type']}`\n"
                f"• **Function:** `{state['bot_function']}`\n"
                f"• **Commands:** `{state['bot_commands']}`\n"
                f"• **Budget:** ₹{state['budget']}\n"
                f"• **Extra:** `{state['extra']}`",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
                    ]
                ]),
                parse_mode=ParseMode.MARKDOWN
            )

            del user_states[user_id]

        elif message.text.lower() == "cancel":
            del user_states[user_id]
            await message.reply("❌ Your order has been **cancelled**.")

@bot.on_callback_query(filters.regex(r"^(approve|reject)_(\d+)$") & filters.user(SUDO_USERS))
async def handle_order_decision(_, query):
    action, user_id = query.data.split("_")
    user_id = int(user_id)
    order_id = random.randint(1000, 9999)
    order = await pending_col.find_one({"user_id": user_id})

    if not order:
        await query.message.edit_text("❗ Order already processed or not found.")
        return

    if action == "approve":
        completed_data = {
            "_id": user_id,
            "status": "approved",
            "order_id": order_id,
            "bot_name": order["bot_name"],
            "bot_type": order["bot_type"],
            "bot_function": order["bot_function"],
            "bot_commands": order["bot_commands"],
            "budget": order["budget"],
            "extra": order["extra"]
        }
        await completed_col.insert_one(completed_data)
        await bot.send_message(user_id, "✅ Your bot order has been **approved!** Our team will contact you soon.")
        await query.message.edit_text("✅ Order has been **approved.**")

    elif action == "reject":
        await bot.send_message(user_id, "❌ Your bot order has been **rejected.** Reach out to support for more details.")
        await query.message.edit_text("❌ Order has been **rejected.**")

    await pending_col.delete_one({"user_id": user_id})
