from KuroAI import KuroAI 
from pyrogram import Client, filters 
from pyrogram.enums import ChatType 
from config import * 
from KuroAI import HANDLERS 
from KuroAI.KUROMAIN.DATABASE import auth_col.



@KuroAI.on_message(filters.command("report", prefixes=HANDLERS)) 
async def report_to_admins(client, message):
  user_id = message.from_user.id 
  authorized = await auth_col.find_one({"user_id": user_id}) 

  if not authorized:
    await message.reply_text("SAX 🎷🎷🎷\n❌ NOT AUTHORIZED ") 
    return 

  if not len(message.command) >= 2:
    await message.reply_text(" SAX 🎷🎷🎷\n❌GIVE REASON ALSO") 
    return 
  reason = message.command[1:] 

  await message.reply_text("GOOD 👍 \n REPORT SENDED TO SUDO USERS") 

  for user in SUDO_USERS:
    await KuroAI.send_message(chat_id=user, text=f"💥NEW REPORT FROM {message.from_user.first_name}\nQUERY={reason}") 

  except Exception as e:
     await message.reply_text("☣️ERROR SENDING REPORT") 
     print(f"ERROR FOUND IN REPORT OF {message.from_user.username}\n[ERROR]==>{e}") 

