from pyrogram import filters
from pyrogram.types import Message
from bot import CMD_TRIGGER, help_msgs, UserBot, SUDO_TRIGGER, SUDO_USERS, MyClient
import os

MODULE_NAME = "logger"

HELP_TEXT = f"""Module: **{MODULE_NAME.capitalize()}**

**Commands:**

`{CMD_TRIGGER}log` - get the log file.
`{CMD_TRIGGER}help {MODULE_NAME}` - Show this message.
"""

help_msgs[MODULE_NAME] = HELP_TEXT

@UserBot.on_message((filters.command("log", CMD_TRIGGER) & filters.me) | (filters.command("log", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def getlogHandler(bot: MyClient, message: Message):
    if not os.path.exists("log.txt"):
        return await bot.editMsg(message, text="No log file found.")
    await message.reply_document("log.txt", caption="Here is the log file.")
    await message.delete()