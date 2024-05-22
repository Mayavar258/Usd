from pyrogram import idle
from bot import logger, UserBot, LOG_CHAT, Bot, SUDO_USERS

async def startBot():
    await UserBot.start()
    await Bot.start()
    logger.info(f"Total {len(SUDO_USERS)} sudo users")
    await Bot.send_message(chat_id=LOG_CHAT, text="Bot started successfully.")
    await idle()
    await UserBot.stop()
    await Bot.stop()

UserBot.run(startBot())
