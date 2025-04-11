#AL things imported
from config import * 
from pyrogram import Client, filters 
import os 
import sys 
import logging

# LOGGING
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
                                                    logging.StreamHandler()], format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)

HANDLERS = [".", "!", "/", "#", "$", "%", "&", "*", "?"]
MY_VERSION = 1.5.30

#IF USER DON'T GET ANY OF THESE THINGS IN ENVIRONNEMENT
if not (API_ID, API_HASH, TOKEN):
  raise "Varaibles not found"

#CREATING A CLIENT
KuroAI = Client(
  "KuroAI-COLXproMain", 
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="KuroAI/KUROMAIN/COMMAND") 
  
)
