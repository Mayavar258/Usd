from bot import CMD_TRIGGER, LOG_CHAT, help_msgs, LOGGER, UserBot, Bot, MyClient, SUDO_TRIGGER, SUDO_USERS
from bot.helpers import db, get_user
from pyrogram import filters, enums
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid, ChannelInvalid
from pyrogram.types import Message, ChatPermissions


MODULE_NAME = "antispam"
HELP_TEXT = f"""Module: **{MODULE_NAME.capitalize()}**

**Commands:**

`{CMD_TRIGGER}gban` - Globally ban a user.
`{CMD_TRIGGER}gmute` - Globally mute a user.
`{CMD_TRIGGER}ungban` - Unban a user.
`{CMD_TRIGGER}ungmute` - Unmute a user.
`{CMD_TRIGGER}checkgbanned` - Check if a user is gbanned.
`{CMD_TRIGGER}checkgmuted` - Check if a user is gmuted.
"""

help_msgs[MODULE_NAME] = HELP_TEXT
logger = LOGGER(__name__)

async def un_ban_mute(user_id: int, client: MyClient, msg: Message, task="unban"):
    msg = await client.editMsg(msg, text=f"**Un{task.capitalize()}ing** {user_id}")
    if task == "unban":
        isRestricted = await db.is_gbanned(user_id)
    else:
        isRestricted = await db.is_gmuted(user_id)
    if not isRestricted:
        if task == "unban":
            return await msg.edit(text="User is not gbanned.")
        else:
            return await msg.edit(text="User is not gmuted.")
    try:
        for x in isRestricted["chat_ids"]:
            try:
                await client.unban_chat_member(x, user_id)
            except Exception as e:
                await msg.edit(text=f"**Error:** {e}")
    except Exception as e:
        return await msg.edit(text=f"**Error:** {e}")
    if task == "unban":
        await db.remove_gban(user_id)
    else:
        await db.remove_gmute(user_id)
    await msg.edit(text=f"**Un{task.capitalize().strip('e')}ed** {user_id}")
    await client.send_message(chat_id=LOG_CHAT, text=f"Globally {task} {user_id} successfully.")


async def add_ban_mute(user_id, client: MyClient, task="ban", chats=[], from_user=None, DbInfo={}):
    if len(chats) == 0:
        chats = await client.get_common_chats(user_id)
    if not from_user:
        from_user = await client.get_users(user_id)
    gbanned_chats = []
    for chat in chats:
        if chat.id in DbInfo.get("chat_ids", []):
            continue
        try:
            if task == "ban":
                await chat.ban_member(user_id)
                gbanned_chats.append(chat.id)
            else:
                await chat.restrict_member(user_id, ChatPermissions())
                gbanned_chats.append(chat.id)
            await client.send_message(chat_id=LOG_CHAT,text=
                    r"\\**#Antispam_Log**//"
                    f"\n**User:** [{from_user.first_name}](tg://user?id={user_id})\n"
                    f"**User ID:** `{user_id}`\n"
                    f"**UserName:** `{from_user.username}`\n"
                    f"**Chat:** {chat.title}\n"
                    f"**Chat ID:** `{chat.id}`\n"
                    f"\n#{'GBAN' if task=='ban' else 'GMUTE'} #{user_id}")
        except (ChatAdminRequired, UserAdminInvalid, ChannelInvalid):
            pass
        except Exception as e:
            await client.send_message(chat_id=LOG_CHAT, text=f"**Error:** {e}")
    if task=="ban":
        await db.add_gban(user_id, gbanned_chats)
    else:
        await db.add_gmute(user_id, gbanned_chats)


@UserBot.on_message((filters.command(["gban"], CMD_TRIGGER) & filters.me) | (filters.command("gban", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def gbanHandler(bot: MyClient, message: Message):
    if user:=(await get_user(message, bot)):
        if user.id == message.from_user.id:
            return await message.edit(text="You can't gban yourself.")
        await add_ban_mute(user.id, bot, "ban", from_user=user)
        await bot.editMsg(message, text=f"**GBanned** {user.mention}")


@UserBot.on_message((filters.command("gmute", CMD_TRIGGER) & filters.me) | (filters.command("gmute", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def gmuteHandler(bot: MyClient, message: Message):
    if user:=(await get_user(message, bot)):
        if user.id == message.from_user.id:
            return await message.edit(text="You can't gmute yourself.")
        await add_ban_mute(user.id, bot, "mute", from_user=user)
        await bot.editMsg(message, text=f"**GMuted** {user.mention}")

@UserBot.on_message((filters.command("ungban", CMD_TRIGGER) & filters.me) | (filters.command("ungban", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def ungbanHandler(bot: MyClient, message: Message):
    if user:=(await get_user(message, bot)):
        await un_ban_mute(user.id, bot, message, "unban")

@UserBot.on_message((filters.command("ungmute", CMD_TRIGGER) & filters.me) | (filters.command("ungmute", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def ungmuteHandler(bot: MyClient, message: Message):
    if user:=(await get_user(message, bot)):
        await un_ban_mute(user.id, bot, message, "ungmute")

@UserBot.on_message((filters.command("checkgbanned", CMD_TRIGGER) & filters.me) | (filters.command("checkgbanned", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def CheckifGbanned(client: MyClient, message: Message):
    if user:=(await get_user(message, client)):
        if banned:= (await db.is_gbanned(user.id)):
            return await client.editMsg(text=f"**{user.mention}** is **GBanned**\n{'In chats: ' + ', '.join([str(x) for x in banned['chat_ids']]) if banned.get('chat_ids') else ''}")
        return await client.editMsg(message, text=f"**{user.mention}** is **Not GBanned**")

@UserBot.on_message((filters.command("checkgmuted", CMD_TRIGGER) & filters.me) | (filters.command("checkgmuted", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def CheckifGmuted(client: MyClient, message: Message):
    if user:=(await get_user(message, client)):
        if await db.is_gmuted(user.id):
            return await client.editMsg(message, text=f"**{user.mention}** is **GMuted**")
        return await client.editMsg(message, text=f"**{user.mention}** is **Not GMuted**")

@Bot.on_chat_member_updated()
async def autoJoinHandler(client: MyClient, message: Message):
    if member:=message.new_chat_member:
        user = member.user
        if BanInfo:=(await db.is_gbanned(user.id)):
            if member.status == enums.ChatMemberStatus.BANNED:
                return
            logger.info(f"GBanned user {user.id} joined {message.chat.id}")
            await add_ban_mute(user.id, MyClient, "ban", chats=[message.chat], from_user=user, DbInfo=BanInfo)
            if message.chat.type != enums.ChatType.CHANNEL:
                await client.send_message(chat_id=message.chat.id, text=f"**{user.mention}** is **GBanned**")
        elif (message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]) & bool(BanInfo:=(await db.is_gmuted(user.id))):
            if member.status == enums.ChatMemberStatus.RESTRICTED:
                return
            await add_ban_mute(user.id, MyClient, "mute", chats=[message.chat], from_user=user, DbInfo=BanInfo)