from pyrogram.types import Message
from bot import MyClient

def extractArgs(msg: Message):
    return msg.text.split(" ")[1:]

async def get_user(msg: Message, client: MyClient):
    if msg.reply_to_message:
        return msg.reply_to_message.from_user
    elif args:= extractArgs(msg):
        try:
            args[0] = int(args[0])
        except:
            pass
        try:
            return await client.get_users(args[0])
        except:
            await client.editMsg(msg, text="Invalid user ID, provide a valid user id or username.")
            return None
    else:
        await client.editMsg(msg, text="Reply to a user or provide a user ID.")
        return None