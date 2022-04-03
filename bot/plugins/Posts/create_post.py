from datetime import datetime
from pyrogram import filters, Client
from bot.utils.logging import logger
from bot.utils.parser import find_device, parse_post_links

banner_photos = [
    'AgACAgUAAxkBAANMYkmRZxtdejAhIg0nYHbXUy7jd8gAAtWuMRuIsUlW1XO8VP_oLZcACAEAAwIAA20ABx4E'  # red
]


@Client.on_message(filters.command(commands=(["release"])))
async def create_post(client, message):
    logger.info("Someone called for me?")
    if len(message.command) < 2:
        await message.reply_text("Feed me the links senpai")
        return

    parsed_links: dict = parse_post_links(message.command[1:])
    date = datetime.today().strftime('%Y-%m-%d')
    device = find_device(message.command[1])

    caption = f"""
    KOSP 12.1 | OFFICIAL

    Maintainers: @darknanobot
    Device: {device}
    Date: {date}

    Download: 
    *   [Rom]({parsed_links["rom"][0]})
    *   [Fastboot]({parsed_links["fastboot"][0]})
    *   [Incremental]({parsed_links["incremental"][0]})
    *   [Boot]({parsed_links["boot"][0]})

    [Changelog](https://raw.githubusercontent.com/AOSP-Krypton/ota/A12/{device}/changelog_{date})

    Support group
    *   [Official](https://t.me/kryptonaosp)
    *   [Device](https://t.me/kospOP7P)
    """

    await client.send_photo(chat_id=message.chat.id,
                            photo=banner_photos[0],
                            parse_mode="md",
                            caption=caption)
