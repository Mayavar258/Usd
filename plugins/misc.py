from pyrogram import filters
from pyrogram.types import Message
from bot import CMD_TRIGGER, START_TIME, help_msgs, UserBot, SUDO_TRIGGER, SUDO_USERS, MyClient
from bot.helpers import db, get_user
import time

MODULE_NAME = "misc"

HELP_TEXT = f"""Module: **{MODULE_NAME.capitalize()}**

**Commands:**

`{CMD_TRIGGER}ping` - Check the bot's ping.
`{CMD_TRIGGER}whois` - Get info about a user.
`{CMD_TRIGGER}alive` - Check if the bot is alive.
`{CMD_TRIGGER}help {MODULE_NAME}` - Show this message.
`{CMD_TRIGGER}id` - Get user and chat ID.
"""

help_msgs[MODULE_NAME] = HELP_TEXT

@UserBot.on_message((filters.command("ping", CMD_TRIGGER) & filters.me) | (filters.command("ping", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def pingChecker(bot: MyClient, message: Message):
    startTime = time.time()
    await bot.editMsg(message, text=f"Pong!\n{time.time() - startTime}ms")

@UserBot.on_message((filters.command("whois", CMD_TRIGGER) & filters.me) | (filters.command("whois", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def whoisInfo(bot: MyClient, message: Message):
    if not (user := await get_user(message, bot)):
        return await bot.editMsg(message, text="Reply to a user or provide a user ID.")
    await bot.editMsg(message, text=f"""**User Info:**
**First Name:** {user.first_name}
**Last Name:** {user.last_name}
**Username:** {'@'+user.username if user.username else 'Not Found'}
**DC ID:** {user.dc_id}
**User ID:** {user.id}
**Last Seen:** {user.last_online_date}
**Is Bot:** {user.is_bot}

**DB Info:**
**Is Gmuted:** {'Yes' if bool(await db.is_gmuted(user.id)) else 'No'}
**Is Gbanned:** {'Yes' if bool(await db.is_gbanned(user.id)) else 'No'}""")

@UserBot.on_message(filters.command("alive", CMD_TRIGGER) & filters.me)
async def aliveHandler(bot: MyClient, message: Message):
    await bot.editMsg(message, 
        text=f"**Bot is alive!**\n**Uptime:** {time.time() - START_TIME:.0f}s"
    )

@UserBot.on_message((filters.command("id", CMD_TRIGGER) & filters.me) | (filters.command("id", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def getIdHandler(bot: MyClient, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    chat_id = message.chat.id
    await bot.editMsg(message, text=f"**User ID:** `{user_id}`\n**Chat ID:** `{chat_id}`")