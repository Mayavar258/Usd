from pyrogram import filters
from pyrogram.types import Message
from bot import CMD_TRIGGER, help_msgs, UserBot, SUDO_TRIGGER, SUDO_USERS, MyClient
from bot.helpers import extractArgs


@UserBot.on_message((filters.command("modules", CMD_TRIGGER) & filters.me) | (filters.command("modules", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def showModules(bot: MyClient, message: Message):
    modules = ", ".join([f"`{module}`" for module in help_msgs.keys()])
    await bot.editMsg(message, text=f"**Available Modules:**\n{modules}")

@UserBot.on_message((filters.command("help", CMD_TRIGGER) & filters.me) | (filters.command("help", SUDO_TRIGGER) & filters.user(SUDO_USERS)))
async def helpHandler(bot: MyClient, message: Message):
    if args:= extractArgs(message):
        module_name = args[0].lower()
        if module_name in help_msgs:
            await bot.editMsg(message, text=help_msgs[module_name])
        else:
            await bot.editMsg(message, text=f"Invalid module name, check the available modules using {CMD_TRIGGER}modules")
    else:
        await showModules(bot, message)