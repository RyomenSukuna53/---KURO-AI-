from KuroAI import KuroAI 
from KuroAI.KUROMAIN.DATABASE import completed_col 
from pyrogram import Client, filters 
from pyrogram.enums import ParseMode 
from KuroAI import HANDELRS
from config import SUDO_USERS

@KuroAI.on_message("completed", prefixes=HANDLERS) & filters.user(SUDO_USERS)) 
async def order_completed(client, filters):
  user_id = int(message.command[1]) 

  if not user_id:
    await message.reply_text("❌ invalid syntax\nUSAGE:-»\n\t/completed <user_id>") 
    return 

  compl
