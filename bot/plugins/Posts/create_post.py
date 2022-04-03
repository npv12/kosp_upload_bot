from datetime import datetime
from typing import List
from pyrogram import filters, Client
from bot.database.maintainer_details import maintainer_details
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

    download_link_str: str = "Download:\n"

    possible_links = ["rom", "fastboot", "incremental", "boot"]

    for link_type in possible_links:

        if len(parsed_links[link_type]) > 0:
            download_link_str += f"""
    *    [{link_type.capitalize()}]({parsed_links[link_type][0]}) """
            for i in range(1, len(parsed_links[link_type])):
                download_link_str += f"[Mirror {i}]({parsed_links[link_type][i]}) "

    date = datetime.today().strftime('%Y-%m-%d')
    device = find_device(message.command[1])

    maintainers: List[dict] = maintainer_details.get_maintainers(device)
    maintainer_str: str = ""
    for maintainer in maintainers:
        maintainer_str += f"[{maintainer['name']}](tg://user?id={maintainer['user_id']}) "

    device_support_group = maintainer_details.get_device_support_group(device)

    caption = f"""
    KOSP 12.1 | OFFICIAL

    Maintainers: {maintainer_str}

    Device: {device}
    Date: {date}

    {download_link_str}

    [Changelog](https://raw.githubusercontent.com/AOSP-Krypton/ota/A12/{device}/changelog_{date})

    Support group
    
    *   [Official](https://t.me/kryptonaosp)"""

    if device_support_group:
        caption += f"""
    *   [Device]({device_support_group})"""

    await client.send_photo(chat_id=message.chat.id,
                            photo=banner_photos[0],
                            parse_mode="md",
                            caption=caption)
