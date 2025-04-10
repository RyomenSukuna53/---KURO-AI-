from pyrogram import Client, filters 
from KuroAI import KuroAI as bot 
from KuroAI import HANDLERS



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
        return f"An error occurred: {str(e)}"


