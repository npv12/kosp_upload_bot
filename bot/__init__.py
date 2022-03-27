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
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

    # OneDrive details
    CLIENT_ID = os.environ.get("CLIENT_ID", None)
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
    TENANT = os.environ.get("TENANT", None)
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN", None)

else:
    #Config File
    config_file = "config.ini"
    config = ConfigParser()
    config.read(config_file)

    # Pyrogram details
    API_ID = config.get(NAME, 'API_ID')
    API_HASH = config.get(NAME, "API_HASH")
    BOT_TOKEN = config.get(NAME, "BOT_TOKEN")

    # OneDrive details
    CLIENT_ID = config.get(NAME, "CLIENT_ID")
    CLIENT_SECRET = config.get(NAME, "CLIENT_SECRET")
    TENANT = config.get(NAME, "TENANT")
    REFRESH_TOKEN = config.get(NAME, "REFRESH_TOKEN")

print("Env set properly")