from datetime import datetime
import random
from typing import List
from pyrogram import filters, Client
from bot.database.maintainer_details import maintainer_details
from bot.utils.logging import logger
from bot.utils.parser import find_device, find_kosp_ver, parse_post_links

banner_photos = [
    {
        "follow":
        'https://kosp.e11z.net/d/banners/Blue%20Theme/Follow%20us.png',
        "banner":
        'https://kosp.e11z.net/d/banners/Blue%20Theme/KOSP%20banner.png',
        "support":
        'https://kosp.e11z.net/d/banners/Blue%20Theme/Support%20us.png'
    },  # blue
    {
        "follow":
        'https://kosp.e11z.net/d/banners/Green%20Theme/Follow%20us.png',
        "banner":
        'https://kosp.e11z.net/d/banners/Green%20Theme/KOSP%20banner.png',
        "support":
        'https://kosp.e11z.net/d/banners/Green%20Theme/Support%20us.png'
    },  # Green
    {
        "follow":
        'https://kosp.e11z.net/d/banners/Red%20Theme/Follow%20us.png',
        "banner":
        'https://kosp.e11z.net/d/banners/Red%20Theme/KOSP%20banner.png',
        "support":
        'https://kosp.e11z.net/d/banners/Red%20Theme/Support%20us.png'
    },  # Red,
    {
        "follow":
        'https://kosp.e11z.net/d/banners/Rose%20Theme/Follow%20us.png',
        "banner":
        'https://kosp.e11z.net/d/banners/Rose%20Theme/KOSP%20banner.png',
        "support":
        'https://kosp.e11z.net/d/banners/Rose%20Theme/Support%20us.png'
    },  #Rose
    {
        "follow":
        'https://kosp.e11z.net/d/banners/Violet%20Theme/Follow%20us.png',
        "banner":
        'https://kosp.e11z.net/d/banners/Violet%20Theme/KOSP%20banner.png',
        "support":
        'https://kosp.e11z.net/d/banners/Violet%20Theme/Support%20us.png'
    },  # Violet
    {
        "follow":
        'https://kosp.e11z.net/d/banners/Yellow%20Theme/Follow%20us.png',
        "banner":
        'https://kosp.e11z.net/d/banners/Yellow%20Theme/KOSP%20banner.png',
        "support":
        'https://kosp.e11z.net/d/banners/Yellow%20Theme/Support%20us.png'
    },  # Yellow
]


@Client.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited
                   & ~filters.forwarded
                   & filters.command(commands=(["release"])))
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

    device = find_device(message.command[1])

    maintainers: List[dict] = maintainer_details.get_maintainers(device)
    maintainer_str: str = ""
    for maintainer in maintainers:
        maintainer_str += f"[{maintainer['name']}](tg://user?id={maintainer['user_id']}) "

    device_support_group = maintainer_details.get_device_support_group(device)

    kosp_version = find_kosp_ver(message.command[1])

    caption = f"""
    KOSP {kosp_version} | Android 12.1 | OFFICIAL

    Maintainers: {maintainer_str}

    Device: {device}
    Date: {datetime.today().strftime('%d-%m-%y')}

    {download_link_str}

    [Changelog](https://raw.githubusercontent.com/AOSP-Krypton/ota/A12/{device}/changelog_{datetime.today().strftime('%Y_%m_%d')})

    Support group
    
    *   [Official](https://t.me/kryptonaosp)"""

    if device_support_group:
        caption += f"""
    *   [Device]({device_support_group})"""

    try:

        await client.send_photo(chat_id=message.chat.id,
                                photo=banner_photos[random.randint(
                                    0, 5)]["banner"],
                                parse_mode="md",
                                caption=caption)
    except:
        await message.reply_text("Something went wrong")
        return
