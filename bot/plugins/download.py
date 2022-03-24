from pyrogram import filters, Client

from bot.document_processor.base import DocumentProccesor
from bot.document_processor.factory import DocumentProcessorFactory


@Client.on_message(
    filters.chat(-1001755612783) & filters.command(
        commands=(["Download", "download", "Downloads", "downloads"])))
async def download(client, message):

    if (len(message.command) == 1):
        await message.reply_text(
            "No download link was provided.\nPlease provide one")
        return

    download_url: str = message.command[1]
    handler: DocumentProccesor = DocumentProcessorFactory.create_document_processor(
        download_url)
    replied_message = await message.reply_text("Starting the download for you")
    file_name = await handler.download(download_url, replied_message)
    await replied_message.edit_text("Downloaded file at " + file_name)


@Client.on_message(~filters.chat(-1001755612783) & filters.command(
    commands=(["Download", "download", "Downloads", "downloads"])))
async def download_forbidden(client, message):

    await message.reply_text("You are not allowed to use this command")


@Client.on_message(filters.command(commands=(["Mirror", "mirror"])))
async def mirror(client, message):

    if (len(message.command) == 1):
        await message.reply_text(
            "No download link was provided.\nPlease provide one")
        return

    download_url: str = message.command[1]
    handler: DocumentProccesor = DocumentProcessorFactory.create_document_processor(
        download_url)
    replied_message = await message.reply_text("Starting the download for you")
    file_name = await handler.download(download_url, replied_message)
    await handler.upload(file_name, replied_message)