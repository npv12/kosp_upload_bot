import shutil
from pyrogram import filters, Client
import bot
from bot.constants import TEMP_FOLDER_PATH

from bot.document_processor.base import DocumentProccesor
from bot.document_processor.factory import DocumentProcessorFactory
from bot.utils.logging import logger


@Client.on_message(filters.command(commands=(["Mirror", "mirror"])))
async def mirror(client: bot, message):

    logger.info("God asked me to mirror something")

    if (len(message.command) == 1):
        logger.info("No download URL were provided")
        await message.reply_text(
            "No download link was provided.\nPlease provide one")
        return

    download_url: str = message.command[1]
    logger.info("Found download url as {download_url}")
    replied_message = await message.reply_text("Starting the download for you")

    try:
        handler: DocumentProccesor = DocumentProcessorFactory.create_document_processor(
            download_url, replied_message)

        file_name = await handler.download(message.from_user.id, download_url)
        logger.info(f"Downloaded file at {file_name}")

        await replied_message.edit_text(
            "Downloaded successfully. \nStarting upload now")

        url: str = await handler.upload(file_name)
        logger.info(f"Uploaded file at {url}")
        shutil.rmtree(TEMP_FOLDER_PATH)
        await replied_message.edit_text(
            f"Successfully uploaded file. you can find it at {url}")

    except Exception as e:
        logger.exception(e)
        await replied_message.edit_text(
            "Mirror failed.\nPlease check the link and try again")