#AL things imported
from config import * 
from pyrogram import Client, filters 
import os 
import sys 
import logging

# LOGGING
logging.basicConfig(
  format="[KuroAI-Beta] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)

HANDLERS = [".", "!", "/", "#", "$", "%", "&", "*", "?"]


#IF USER DON'T GET ANY OF THESE THINGS IN ENVIRONNEMENT
if not (API_ID, API_HASH, TOKEN):
  raise "Varaibles not found"

#CREATING A CLIENT
KuroAI = Client(
  "KuroAI-COLXproMain", 
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="/KURO-AI/KURO-MAIN/COMMAND") 
  
)
