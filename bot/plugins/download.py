from pyrogram import filters, Client

from bot.document_processor.base import DocumentProccesor
from bot.document_processor.factory import DocumentProcessorFactory


@Client.on_message(
    filters.command(
        commands=(["Download", "download", "Downloads", "downloads"])))
async def download(client, message):

    if (len(message.command) == 1):
        await message.reply_text(
            "No download link was provided.\nPlease provide one")
        return

    download_url: str = message.command[1]
    handler: DocumentProccesor = DocumentProcessorFactory.create_document_processor(
        download_url)
    await message.reply_text("Starting the download for you")
    handler.download(download_url)
    await message.reply_text("Download is complete")