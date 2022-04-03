from datetime import datetime
import random
from typing import List
from pyrogram import filters, Client
from bot.database.maintainer_details import maintainer_details
from bot.utils.logging import logger
from bot.utils.parser import find_device, parse_post_links

banner_photos = [
    {
        "follow":
        'AgACAgUAAx0CaKSGbwAD0WJJsa0MSm8ETVFaEQkISbvjZfbpAAIlsDEbGwdRVhCZYB2xUXiaAAgBAAMCAAN4AAceBA',
        "banner":
        'AgACAgUAAx0CaKSGbwAD0mJJsi0-sDCjn4A7I-YVtlrjNMeAAAImsDEbGwdRVoGTZQjs0v6AAAgBAAMCAAN5AAceBA',
        "support":
        'AgACAgUAAx0CaKSGbwAD02JJsj6StsL-l6g8TKOzENsnfC16AAInsDEbGwdRVszCOtHSyIQjAAgBAAMCAAN4AAceBA'
    },  # blue
    {
        "follow":
        'AgACAgUAAx0CaKSGbwAD1GJJsm0lIVGfP3_AcPspDp5cO1rSAAIosDEbGwdRViH-GHZCuAV2AAgBAAMCAAN4AAceBA',
        "banner":
        'AgACAgUAAx0CaKSGbwAD1WJJsnL5d72HDtdL04mJQl2qw1iRAAIpsDEbGwdRVubBSVPuTU8mAAgBAAMCAAN5AAceBA',
        "support":
        'AgACAgUAAx0CaKSGbwAD1mJJsnaABcgU0aVefOdNHPaPkzcxAAIqsDEbGwdRVnA670y1qan-AAgBAAMCAAN4AAceBA'
    },  # Green
    {
        "follow":
        'AgACAgUAAx0CaKSGbwAD12JJsp9JvE0AAXSK1dpMU9VqZBTfwAACK7AxGxsHUVaTe7_Y1hnw5gAIAQADAgADeAAHHgQ',
        "banner":
        'AgACAgUAAx0CaKSGbwAD2GJJsqRQYJjmnBaBqLyvQha_IZkIAALVrjEbiLFJVtVzvFT_6C2XAAgBAAMCAAN5AAceBA',
        "support":
        'AgACAgUAAx0CaKSGbwAD2WJJsqtc3dM17ldgrCzOUJs0Gg8HAAIssDEbGwdRVmWTlGmDE4HmAAgBAAMCAAN4AAceBA'
    },  # Red,
    {
        "follow":
        'AgACAgUAAx0CaKSGbwAD2mJJstVkvsCiuJysDpBm9BhN5jgFAAItsDEbGwdRVjC39bTSNXNmAAgBAAMCAAN4AAceBA',
        "banner":
        'AgACAgUAAx0CaKSGbwAD22JJstncg_XgyMPYigQHiIp0664pAAIusDEbGwdRVjE-QyNuRsytAAgBAAMCAAN5AAceBA',
        "support":
        'AgACAgUAAx0CaKSGbwAD3GJJst00e4PN7W7T8KxYPZPXA2pyAAIvsDEbGwdRVoS_DFS9iBAEAAgBAAMCAAN4AAceBA'
    },  #Rose
    {
        "follow":
        'AgACAgUAAx0CaKSGbwAD3WJJswPqS7rdE2tvzdbDy0s27Kz2AAIwsDEbGwdRVtjg6O4c5zshAAgBAAMCAAN4AAceBA',
        "banner":
        'AgACAgUAAx0CaKSGbwAD3mJJswg_NsBcEfuQjgE5GjQZw837AAIxsDEbGwdRVpT5a-04BM4aAAgBAAMCAAN5AAceBA',
        "support":
        'AgACAgUAAx0CaKSGbwAD32JJswsw6Csn954jDzj4smh0dZd9AAIysDEbGwdRVu4V1_Dk6EwQAAgBAAMCAAN4AAceBA'
    },  # Violet
    {
        "follow":
        'AgACAgUAAx0CaKSGbwAD4GJJsw5F0-5O_H63fL0g0kn4i_a-AAIzsDEbGwdRVvqmBSxNp84-AAgBAAMCAAN4AAceBA',
        "banner":
        'AgACAgUAAx0CaKSGbwAD4WJJsxHrjtIDFBCOaCf0-fhUhprvAAI0sDEbGwdRVtYKZQGtoq-VAAgBAAMCAAN5AAceBA',
        "support":
        'AgACAgUAAx0CaKSGbwAD4mJJsxRpLQjx381KMZgNAuWfPO-hAAI1sDEbGwdRVsJJ6im9aCNOAAgBAAMCAAN4AAceBA'
    },  # Green
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
                            photo=banner_photos[random.randint(0,
                                                               5)]["banner"],
                            parse_mode="md",
                            caption=caption)
