from pyrogram import filters, Client
from bot.utils.logging import logger
from bot.database.maintainer_details import maintainer_details


@Client.on_message(filters.command(commands=(["add"])))
async def add_maintainer(client, message):
    logger.info("Lets add a new maintainer")
    requester_id = message.from_user.id
    maintainer_id: int
    device: str
    if not message.reply_to_message and len(message.command) < 1:
        await message.reply_text(
            "Reply to a user or specify their userID to add them as a maintainer"
        )
        return

    if message.reply_to_message:
        maintainer_id = message.reply_to_message.from_user.id
        device = message.command[1]

    elif len(message.command) == 2:
        maintainer_id = int(message.command[1])
        device = message.command[2]

    else:
        await message.reply_text("Please specify a device")
        return

    await message.reply_text("Adding a maintainer")
    maintainer_details.add_maintainer(requester_id, maintainer_id, device)