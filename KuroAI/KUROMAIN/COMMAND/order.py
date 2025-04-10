from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from KuroAI import KuroAI as bot
from config import OWNER_ID, SUDO_USERS
from KuroAI.KUROMAIN.DATABASE import order_col, pending_col, completed_col, auth_col# your imported mongo cols
from KuroAI import HANDLERS 
import random
from pyrogram.emums import ChatType, ParseMode
user_states = {}

@bot.on_message(filters.command("order", prefixes=HANDLERS))
async def start_order(_, message: Message):
    user_id = message.from_user.id
    auth_user = auth_col.find_one({"_id": user_id}) 

    if not auth_user:
      await message.reply_text("❌NOT AUTHORIZED ") 
      return 
  
    user_states[user_id] = {"step": "name", "user_id": user_id}
    await message.reply("Enter your bot name:")

@bot.on_message(filters.text)
async def handle_order_step(_, message: Message):
    user_id = message.from_user.id
    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state["step"] == "name":
        state["bot_name"] = message.text
        state["step"] = "type"
        await message.reply("Enter bot type (e.g., Music, Game, AI):")

    elif state["step"] == "type":
        state["bot_type"] = message.text
        state["step"] = "budget"
        await message.reply("Enter your budget in ₹:")

    elif state["step"] == "budget":
        state["budget"] = message.text
        state["step"] = "extra"
        await message.reply("Any extra info? Send `/skip` to skip.")

    elif state["step"] == "extra":
        state["extra"] = message.text if message.text != "/skip" else "None"
        state["step"] = "confirm"

        text = (
            f"**Please confirm your order:**\n\n"
            f"**Bot Name:** {state['bot_name']}\n"
            f"**Bot Type:** {state['bot_type']}\n"
            f"**Budget:** ₹{state['budget']}\n"
            f"**Extra Info:** {state['extra']}\n\n"
            "**Type `confirm` to send or `cancel` to discard.**"
        )
        await message.reply(text)

    elif state["step"] == "confirm":
        if message.text.lower() == "confirm":
            order_data = {
                "user_id": user_id,
                "username": message.from_user.username,
                "bot_name": state['bot_name'],
                "bot_type": state['bot_type'],
                "budget": state['budget'],
                "extra": state['extra'],
                "status": "pending"
            }

            await order_col.insert_one(order_data)
            await pending_col.insert_one(order_data)

            await message.reply("✅ Your order has been sent for admin review.")

            await bot.send_message(
                OWNER_ID,
                f"📬 **New Order Request**\n\n"
                f"👤 User: [{message.from_user.first_name}](tg://user?id={user_id})\n"
                f"**Bot Name:** {state['bot_name']}\n"
                f"**Type:** {state['bot_type']}\n"
                f"**Budget:** ₹{state['budget']}\n"
                f"**Extra:** {state['extra']}",
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
            await message.reply("❌ Order cancelled.")


@bot.on_callback_query(filters.regex(r"^(approve|reject)_(\d+)$") & filters.user(SUDO_USERS))
async def handle_order_decision(_, query):
    action, user_id = query.data.split("_")
    user_id = int(user_id)
    order_id = random.randint(1000, 5000) 
    order = await pending_col.find_one({"user_id": user_id})
    if not order:
        await query.message.edit_text("Order not found or already handled.")
        return

    if action == "approve":
        await completed_col.insert_one({**order, "status": "approved", "order_id": order_id})
        await bot.send_message(user_id, "✅ Your bot order has been **approved!** We'll contact you soon.")
        await query.message.edit_text("Order approved.")
    elif action == "reject":
        await completed_col.insert_one({**order, "status": "rejected"})
        await bot.send_message(user_id, "❌ Your bot order has been **rejected.** Contact admin for more info.")
        await query.message.edit_text("Order rejected.")

    await pending_col.delete_one({"user_id": user_id})
  





