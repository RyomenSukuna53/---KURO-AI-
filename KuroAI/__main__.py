#MAIN FILE THAT RUN ALL BOTS COMMANDS ETC 
from pyrogram import Client, filters 
from KuroAI.KUROMAIN import * 
import asyncio 
from KuroAI import *
from KuroAI.KUROMAIN.COMMAND import start, gpt
from KuroAI.KUROMAIN.HELPERS import * 
from KuroAI.KUROMAIN.OWNER_WORKS import auth, unauth, eval


if __name__=="__main__":
    KuroAI.run()

	
