from KURO-AI import KuroAI as bot
from KURO-AI import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from KURO-AI import SUPPORT_CHAT, SUPPORT_CHANNEL

# Mongo DB ya simple set for auth users
authorized_users = set()

# Check if user joined both
async def check_authorized(client, user_id):
    try:
        ch = await client.get_chat_member(SUPPORT_CHANNEL, user_id)
        grp = await client.get_chat_member(SUPPORT_CHAT, user_id)
        return ch.status in ["member", "administrator", "creator"] and grp.status in ["member", "administrator", "creator"]
    except:
        return False

