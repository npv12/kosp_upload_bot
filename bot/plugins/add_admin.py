from pyrogram import filters, Client
from bot.utils.logging import logger
from bot.database.maintainer_details import maintainer_details


@Client.on_message(filters.command(commands=(["addAdmin"])))
async def add_admin(client, message):
    logger.info("Lets add a new admin")
    if not message.reply_to_message:
        await message.reply_text("Reply to a user to add them as a admin")
        return
    await message.reply_text("Adding a admin")
    maintainer_details.add_admin(message.reply_to_message.from_user.id)
