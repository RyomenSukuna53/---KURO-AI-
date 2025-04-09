from config import * 
from pyrogram import Client, filters 


KuroAI = Client(api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

if not (API_ID, API_HASH, TOKEN):
  raise "ENVIRONNEMENT VARIABLES MUST BE SET"

