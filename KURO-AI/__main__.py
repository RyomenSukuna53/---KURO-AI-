#MAIN FILE THAT RUN ALL BOTS COMMANDS ETC 
from pyrogram import Client, filters 
from KURO-MAIN import * 
import asyncio 
from KuroAI import *


if __name__=="__main__":
	KuroAI.run() 
  with KuroAI:
		KuroAI.send_message(chat_id=6239769036, 
												text="BOT STARTED MASTER") 
