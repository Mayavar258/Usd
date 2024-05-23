import os
import logging
import sys
import time
from pyrogram import Client, __version__
from pyrogram.types import Message
from pyrogram.raw.all import layer
from dotenv import load_dotenv

with open("log.txt", "w+") as f:
    f.truncate(0)
    f.close()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name):
    return logging.getLogger(name)

logger = LOGGER(__name__)

if os.path.exists("local.env"):
    logger.info("Using local.env file for environment variables.")
    load_dotenv("local.env", override=True)
else:
    logger.info("its recommended to use local.env file for environment variables.")
#get it from my.telegram.org
API_ID = "27610252"
if not API_ID:
    logger.error("API_ID is not set. Exiting...")
    sys.exit(1)
else:
    try:
        API_ID = int(API_ID)
    except ValueError:
        logger.error("API_ID is not a valid integer. Exiting...")
        sys.exit(1)
API_HASH = "73e16fc08192ba7c1d52d4dc9fa2b220"
# user session string
SESSION_STRING = "BQGlTIwAAfkuMOzEfm3azK-uhHbYkxCDUDR-XSGxcmfqY51JnVBYdttlTs0ckBabyZXEg4Pdr2nYdiuqcg5t8w-1_d11Vdg1DMFDXYGzI1NmSHuW1b0jZVYyEyFYGPY63Jwijyyr6XcpLHJ5N4KGbrNC2YHEVsf3T-VBNjVy1UMyyu12bj9htsjpXBVO8A_4ybP5sZ5E3-PVcsmOdIyW5d9usT2MvbYNfGNVgvKgjIDBk6U3AHd8gSab7RI_SYmm96SnPjcszfxVcjgOqWIMaFJq7wwmcpZJl69Nhz1Puj3WgEO9SmC3ippI0y1BdvdF3J9GzpN2_wRcpOSbp1_Owct79X6StAAAAAE9EwLhAA"
LOG_CHAT = "-1002123026966"

#sudo users
SUDO_USERS = list(int(x) for x in os.environ.get("SUDO_USERS", "5342104384").split(" "))

if not LOG_CHAT:
    logger.error("LOG_CHAT is not set. Exiting...")
    sys.exit(1)
else:
    try:
        LOG_CHAT = int(LOG_CHAT)
    except ValueError:
        logger.error("LOG_CHAT is not a valid chat ID. Exiting...")
        sys.exit(1)

BOT_TOKEN = "6523924964:AAGbSkckJy4TBuj8CXDAEhRMqXE6mbQmybI"

#Database URL, 
MONGO_DB = "mongodb+srv://maya:maya@maya.nepuebg.mongodb.net/?retryWrites=true&w=majority"

#Cmd Trigger
CMD_TRIGGER = os.environ.get("CMD_TRIGGER", ".")
SUDO_TRIGGER = os.environ.get("SUDO_TRIGGER", "!")

if len(CMD_TRIGGER) > 1:
    logger.info("CMD_TRIGGER should be a single character.")
    logger.info("Setting CMD_TRIGGER to default value '.'")
    CMD_TRIGGER = "."

if not any([API_ID, API_HASH, SESSION_STRING, LOG_CHAT, MONGO_DB, BOT_TOKEN]):
    logger.error("One or more env variables are missing. Exiting...")
    sys.exit(1)

START_TIME = time.time()

help_msgs = {} # key: text, value: text

class MyClient(Client):

    def __init__(self, name_, bot_token=None, session_string=None):
        super().__init__(
            name=name_,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            session_string=session_string,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username if me.username else ""
        self.myid = me.id
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
    
    async def editMsg(self, message: Message, text: str) -> Message:
        if self.myid == message.from_user.id:
            return await message.edit_text(text=text)
        else:
            return await message.reply_text(text=text)

UserBot = MyClient(name_="spamBanUser",
               session_string=SESSION_STRING
               )

Bot = MyClient(name_="spamBanBot",
                bot_token=BOT_TOKEN
                )
