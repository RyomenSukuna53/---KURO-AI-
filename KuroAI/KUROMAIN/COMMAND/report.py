from KuroAI import KuroAI
from pyrogram import filters
from config import SUDO_USERS
from KuroAI import HANDLERS
from KuroAI.KUROMAIN.DATABASE import auth_col

@KuroAI.on_message(filters.command("report", prefixes=HANDLERS) & filters.private)
async def report_to_admins(KuroAI, message):
    user_id = message.from_user.id
    user = message.from_user

    try:
        is_authorized = auth_col.find_one({"user_id": user_id})
        if not is_authorized:
            await message.reply_text(
                "⛔️ Access Denied!\n\n"
                "You're not authorized to use this feature."
            )
            return

        if len(message.command) < 2:
            await message.reply_text(
                "⚠️ Missing Report Content!\n\n"
                "Please provide a reason for your report.\n\n"
                "**Usage:** `/report [your issue here]`",
                quote=True
            )
            return

        reason = " ".join(message.command[1:])
        await message.reply_text(
            "✅ Your report has been successfully submitted!\n"
            "Our team will review it shortly.",
            quote=True
        )

        report_text = (
            f"📩 **New Report Received**\n\n"
            f"👤 User: [{user.first_name}](tg://user?id={user.id}) (`{user.id}`)\n"
            f"📝 **Report:** {reason}"
        )

        for sudo_user in SUDO_USERS:
            await KuroAI.send_message(chat_id=sudo_user, text=report_text)

    except Exception as e:
        await message.reply_text(
            "❌ Failed to send your report.\n"
            "Please try again later or contact support."
        )
        print(f"[REPORT ERROR] User: {user.username} | Error: {e}")
