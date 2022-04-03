from pyrogram import filters, Client
from bot.utils.logging import logger


@Client.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited
                   & ~filters.forwarded & filters.command(commands=(["start"]))
                   )
async def start(client, message):
    logger.info("Someone called for me?")
    await message.reply_text("Hello User, I am alive :D")