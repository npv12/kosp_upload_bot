from configparser import ConfigParser
import os
from sys import version_info
import os

__version__ = "1.1"
NAME = 'KOSP'

if version_info[:2] < (3, 6):
    print("KOSP needs version 3.6 or more")
    quit()

print("Setting up ENV")
ENV = bool(os.environ.get('ENV', False))

if ENV:
    # Pyrogram details
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    USERBOT_SESSION = os.environ.get("USERBOT_SESSION", None)

else:
    #Config File
    config_file = "config.ini"
    config = ConfigParser()
    config.read(config_file)

    # Pyrogram details
    API_ID = config.get(NAME, 'API_ID')
    API_HASH = config.get(NAME, "API_HASH")
    BOT_TOKEN = config.get(NAME, "BOT_TOKEN")

print("Env set properly")