# Parses the given file name to the folder it should go to
# It is assumed that file given through here will always be a KOSP file

from typing import List

from bot.utils.logging import logger


def parse_kosp(file_name: str) -> str:
    logger.info(f"Recieved request to parse a file name as {file_name}")
    parts: List[str] = file_name.split("-")[1:]
    android_version = "A" + str(10 + int(float(parts[0])))
    device_name = parts[1]
    logger.info(f"It was parsed as {android_version}/{device_name}")
    return android_version + "/" + device_name

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