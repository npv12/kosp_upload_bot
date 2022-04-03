# Parses the given file name to the folder it should go to
# It is assumed that file given through here will always be a KOSP file

from typing import List

from bot.utils.logging import logger

def find_device(file_name: str) -> str:
    logger.info(f"Recieved request to find a device for {file_name}")

    if "boot_" in file_name:
        device_name = file_name.split("_")[1]
        logger.info(f"It was parsed as {device_name}")
        return device_name

    parts: List[str] = file_name.split("-")[1:]
    device_name = parts[1]
    logger.info(f"It was parsed as {device_name}")
    return device_name