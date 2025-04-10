#MAIN FILE THAT RUN ALL BOTS COMMANDS ETC 
from pyrogram import Client, filters 
from KuroAI.KUROMAIN import * 
import asyncio 
from KuroAI import *
from KuroAI.KUROMAIN.COMMAND import * 
from KuroAI.KUROMAIN.HELPERS import * 
from KuroAI.KUROMAIN.OWNER_WORKS import *


if __name__=="__main__":
	KuroAI.run()
	with KuroAI:
		KuroAI.send_message(chat_id=6239769036, 
												text="BOT STARTED MASTER") 
