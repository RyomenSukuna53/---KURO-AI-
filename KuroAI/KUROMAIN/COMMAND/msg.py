from KuroAI import KuroAI 
from KuroAI import HANDLERS 
from config import *
from pyrogram import filters
from pyrogram.enums import ChatType
from KuroAI.KUROMAIN.DATABASE import auth_col 




@KuroAI.on_message(filters.command("msg", prefixes=HANDLERS) & filters.private & filters.user(SUDO_USERS)) 
async def send_msg_to_user(client, message):
    # Check if minimum 3 parts in command: /msg <user_id> <text...>
    if len(message.command) < 3:
        await message.reply_text("SAX 🎷🎷\nGIVE USER ID AND MESSAGE TEXT")
        return

    reciever = message.command[1]
    query = " ".join(message.command[2:])

    # Validate user_id is digit
    if not reciever.isdigit():
        await message.reply_text("SAX 🎷🎷🎷\n THIS IS NOT A USER ID BRO 😎")
        return

    # Check length (Telegram IDs are usually 9-10 digits)
    if len(reciever) < 8:
        await message.reply_text("SAX 🎷🎷🎷\n IS THIS REALLY A USER ID?")
        return

    # Check if user is authorized
    authorized = await auth_col.find_one({"_id": int(reciever)})
    if not authorized:
        await message.reply_text("SAX 🎷🎷🎷\n THIS USER IS NOT AUTHORIZED")
        return

    # Send message
    try:
        await KuroAI.send_message(chat_id=int(reciever), text=query)
        await message.reply_text("SENDED BOSS")
    except Exception as e:
        await message.reply_text(f"FAILED TO SEND\n\nERROR: `{e}`")

  
