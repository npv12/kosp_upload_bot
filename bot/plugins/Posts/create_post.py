from datetime import datetime
import random
from typing import List
from pyrogram import filters, Client
from bot import CHANNEL_ID
from bot.database.maintainer_details import maintainer_details
from bot.utils.logging import logger
from bot.utils.parser import find_device, find_kosp_ver, parse_post_links

banner_photos = [
    {
        "follow":
        'https://sourceforge.net/projects/kosp/files/banners/Blue-Theme/Follow%20us.png/download',
        "banner":
        'https://sourceforge.net/projects/kosp/files/banners/Blue-Theme/KOSP%20banner.png/download',
        "support":
        'https://sourceforge.net/projects/kosp/files/banners/Blue-Theme/Support%20us.png/download'
    },  # blue
    {
        "follow":
        'https://sourceforge.net/projects/kosp/files/banners/Green-Theme/Follow%20us.png/download',
        "banner":
        'https://sourceforge.net/projects/kosp/files/banners/Green-Theme/KOSP%20banner.png/download',
        "support":
        'https://sourceforge.net/projects/kosp/files/banners/Green-Theme/Support%20us.png/download'
    },  # Green
    {
        "follow":
        'https://sourceforge.net/projects/kosp/files/banners/Red-Theme/Follow%20us.png/download',
        "banner":
        'https://sourceforge.net/projects/kosp/files/banners/Red-Theme/KOSP%20banner.png/download',
        "support":
        'https://sourceforge.net/projects/kosp/files/banners/Red-Theme/Support%20us.png/download'
    },  # Red,
    {
        "follow":
        'https://sourceforge.net/projects/kosp/files/banners/Rose-Theme/Follow%20us.png/download',
        "banner":
        'https://sourceforge.net/projects/kosp/files/banners/Rose-Theme/KOSP%20banner.png/download',
        "support":
        'https://sourceforge.net/projects/kosp/files/banners/Rose-Theme/Support%20us.png/download'
    },  #Rose
    {
        "follow":
        'https://sourceforge.net/projects/kosp/files/banners/Violet-Theme/Follow%20us.png/download',
        "banner":
        'https://sourceforge.net/projects/kosp/files/banners/Violet-Theme/KOSP%20banner.png/download',
        "support":
        'https://sourceforge.net/projects/kosp/files/banners/Violet-Theme/Support%20us.png/download'
    },  # Violet
    {
        "follow":
        'https://sourceforge.net/projects/kosp/files/banners/Yellow-Theme/Follow%20us.png/download',
        "banner":
        'https://sourceforge.net/projects/kosp/files/banners/Yellow-Theme/KOSP%20banner.png/download',
        "support":
        'https://sourceforge.net/projects/kosp/files/banners/Yellow-Theme/Support%20us.png/download'
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

    random_int = random.randint(0, 5)
    random_follow = random.randint(0, 1)
    logger.info(f"Downloading banner {random_int}")
    try:

        await client.send_photo(chat_id=message.chat.id,
                                photo=banner_photos[random_int]["banner"],
                                parse_mode="md",
                                caption=caption)

        await client.send_photo(chat_id=CHANNEL_ID,
                                photo=banner_photos[random_int]["banner"],
                                parse_mode="md",
                                caption=caption)
        if random_follow == 1:
            await client.send_photo(chat_id=CHANNEL_ID,
                                    photo=banner_photos[random_int]["follow"])
        else:
            await client.send_photo(chat_id=CHANNEL_ID,
                                    photo=banner_photos[random_int]["support"])
    except:
        await message.reply_text("Something went wrong")
        return
