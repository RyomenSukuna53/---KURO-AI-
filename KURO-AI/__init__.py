#AL things imported
from config import * 
from pyrogram import Client, filters 

#IF USER DON'T GET ANY OF THESE THINGS IN ENVIRONNEMENT
if not (API_ID, API_HASH, TOKEN):
  raise "Varaibles not found"

#CREATING A CLIENT
KuroAI = Client(api_id=API_ID, 
                api_hash=API_HASH, 
                bot_token=TOKEN, 
                plugins=dict("KURO-MAIN")
               ) 

