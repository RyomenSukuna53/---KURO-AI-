from pyrogram import Client, filters
from pyrogram.types import Message
import io
import contextlib
from config import OWNER_ID, SUDO_USERS
from KuroAI import KuroAI 


@KuroAI.on_message(filters.command("eval") & filters.user(SUDO_USERS))
async def eval_code(client, message: Message):
    if len(message.text.split()) < 2:
        return await message.reply("Please provide code to evaluate.")

    code = message.text.split(" ", 1)[1]

    # Capture the stdout
    stdout = io.StringIO()
    exec_result = ""

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def __aexec(client, message): " +
                "\n " + "\n ".join(f"    {line}" for line in code.split("\n"))
            )
            await locals()["__aexec"](client, message)
    except Exception as e:
        exec_result = f"Error: {e}"
    else:
        exec_result = stdout.getvalue()

    if exec_result:
        await message.reply(f"**Output:**\n`{exec_result}`")
    else:
        await message.reply("No output.")


