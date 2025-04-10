from KuroAI import KuroAI as bot 
from KuroAI.KURO-MAIN.HELPERS.auth import * 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from pyrogram.enums import ParseMode
import asyncio


@bot.on_message(filters.command("start", prefixes=HANDLER))
async def start_command(client, message):
    user = message.from_user.id

    # If not authorized
    if not await check_authorized(client, user):
        await message.reply(
            "**Need Authorization to use this bot.**\n\nJoin both group & channel and try again.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʝσιη ¢нαηηєℓ", url=f"https://{SUPPORT_CHANNEL}")],
                [InlineKeyboardButton("ʝσιη gяσυρ", url=f"https://{SUPPORT_CHAT}")]
            ])
        )
        return

    if user not in authorized_users:
        await message.reply("You're not authorized yet. Ask admin to authorize you.")
        return

    await message.reply("```diff")

# /authorize command (only for sudo/admins)
@bot.on_message(filters.command(["authorize", "auth"], prefixes=HANDLER) & filters.user(SUDO_USERS))
async def authorize_user(client, message):
    if not message.reply_to_message:
        await message.reply("Reply to a user's message to authorize them.")
        return
    user_id = message.reply_to_message.from_user.id
    authorized_users.add(user_id)
    await message.reply(f"Authorized {user_id} successfully.")

# /unauthorize command
@bot.on_message(filters.command(["unauthorize", "unauth"], prefixes=HANDLER) & filters.user(SUDO_USERS))
async def unauthorize_user(client, message):
    if not message.reply_to_message:
        await message.reply("Reply to a user's message to unauthorize them.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id in authorized_users:
        authorized_users.remove(user_id)
        await message.reply(f"Unauthorized {user_id} successfully.")
    else:
        await message.reply("User is not in authorized list.")


