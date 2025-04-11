import aiohttp
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from KuroAI import KuroAI as app
from config import OWNER_ID, SUPPORT_CHAT, SUPPORT_CHANNEL
from KuroAI import HANDLERS
from datetime import datetime
from KuroAI.KUROMAIN.DATABASE import auth_col

MY_VERSION = "1.0"

async def fetch_data(query: str, message: Message) -> str:
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
        url = "https://api.binjie.fun/api/generateStream"
        data = {
            "prompt": query,
            "userId": f"#/chat/{message.from_user.id}",
            "network": True,
            "stream": False,
            "system": {
                "userId": "#/chat/1722576084617",
                "withoutContext": False
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                return await response.text()
    except Exception as e:
        return f"⚠️ Error: `{str(e)}`"

@app.on_message(filters.command("ai", prefixes=HANDLERS), group=5)
async def kuro_ai(_: Client, message: Message):
    user_id = message.from_user.id

    if not await auth_col.find_one({"_id": user_id}):
        return await message.reply(
            "**⛔ Authorization Required!**\n\nJoin both the support channel & group to access the AI.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧬 Join Channel", url=f"https://t.me/{SUPPORT_CHANNEL}")],
                [InlineKeyboardButton("🧠 Join Group", url=f"https://t.me/{SUPPORT_CHAT}")]
            ])
        )

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply("❓ Please provide a query or reply to a message.")

    query = " ".join(message.command[1:]).strip()
    reply_data = ""
    urname = message.from_user.first_name
    urid = message.from_user.id

    if message.reply_to_message:
        replied = message.reply_to_message
        rname = replied.from_user.first_name
        rid = replied.from_user.id
        is_bot = replied.from_user.is_bot
        rmsg = replied.text or "No text available"

        reply_data = (
            f"— Replied Message Context —\n"
            f"• Message: {rmsg}\n"
            f"• User: {rname} | ID: {rid}\n"
            f"• Bot: {is_bot}\n"
            f"• Queried By: {urname} | ID: {urid}\n\n"
        )

        if urid == 6239769036:
            reply_data += "• Special User Detected: 𝙺𝚄𝚁𝙾-𝚁𝙰𝙸𝙹𝙸𝙽 𝙓 黒雷神 — Respect granted.\n\n"

    sys_info = (
        f"\n\n[ 𝗞𝗨𝗥𝗢-𝗔𝗜 𝗦𝗬𝗦𝗧𝗘𝗠 ]\n"
        f"• User: {urname}\n"
        f"• ID: {urid}\n"
        f"• Version: {MY_VERSION}\n"
        f"• Time: {datetime.now().strftime('%B %d %Y, %I:%M %p')}\n"
        f"• Repo: github.com/RyomenSukuna53/GOKU-S_USER_BOT\n"
        f"• Commands: graph.org/KuroAI-Commands-01-30\n"
        f"• Note: You’re a UserBot, not a regular bot.\n"
        f"• Tip: Telegram does not support custom fonts.\n"
    )

    full_query = f"{reply_data}User Query: {query}{sys_info}"

    processing = await message.reply("`🧠 Generating AI response... Please wait.`")
    response = await fetch_data(full_query, message)
    await processing.edit(response, disable_web_page_preview=True)

MOD_NAME = "Gpt"
MOD_HELP = """
• `.ai <query>` — Ask anything from GPT
• `.reply .ai <query>` — Ask based on replied message
"""
