from pyrogram import filters, Client

@Client.on_message(filters.command(commands = (["start"])))
async def start(client, message):
    await message.reply_text("Hello User, I am alive :D")