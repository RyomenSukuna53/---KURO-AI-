from KuroAI import KuroAI as bot 
from KuroAI import HANDLERS 
from config import * 
from pyrogram import Cleint, filters 
from KuroAI.KUROMAIN.DATABASE import *


@bot.on_message(filters.command("clear_orders", prefixes=HANDLERS) & filters.user(SUDO_USERS))
async def clear_all_orders(_, message: Message):
    await order_col.delete_many({})
    await pending_col.delete_many({})
    await completed_col.delete_many({})
    await message.reply("✅ All orders have been cleared from the database.")
