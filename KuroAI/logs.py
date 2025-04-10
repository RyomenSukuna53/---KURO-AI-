import io
import traceback
from subprocess import getoutput as run

from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message

from KuroAI.__init__ import KuroAI as bot
from KuroAI import HANDLERS
from config import OWNER_ID, SUDO_USERS

# Combine OWNER_ID and SUDO_USERS into one set for checking
AUTHORIZED_USERS = set(SUDO_USERS)
AUTHORIZED_USERS.add(OWNER_ID)

@bot.on_message(filters.command(["logs", "log"], prefixes=HANDLERS))
async def tail_logs(_, message: Message):
    if message.from_user.id not in AUTHORIZED_USERS:
        return
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        run_logs = run("tail log.txt")
        text = await message.reply_text("`Getting logs...`")
        await message.reply_text(f"```shell\n{run_logs}```")
        await text.delete()
    except Exception as e:
        await message.reply_text(f"Error:\n{traceback.format_exc()}")

@bot.on_message(filters.command(["flogs", "flog"], prefixes=HANDLERS))
async def full_logs(_, message: Message):
    if message.from_user.id not in AUTHORIZED_USERS:
        return
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
        run_logs = run("cat log.txt")
        text = await message.reply_text("`Sending full logs...`")
        with io.BytesIO(str.encode(run_logs)) as logs:
            logs.name = "log.txt"
            await message.reply_document(document=logs)
        await text.delete()
    except Exception as e:
        await message.reply_text(f"Error:\n{traceback.format_exc()}")
