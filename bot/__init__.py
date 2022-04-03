from configparser import ConfigParser, RawConfigParser
import os
from sys import version_info

from bot.utils.logging import logger

__version__ = "1.1"
NAME = 'KOSP'

if version_info[:2] < (3, 6):
    logger.critical("KOSP needs version 3.6 or more")
    quit()

print("Setting up ENV")
ENV = bool(os.environ.get('ENV', False))

if ENV:
    # Pyrogram details
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

    # OneDrive details
    CLIENT_ID_ONEDRIVE = os.environ.get("CLIENT_ID_ONEDRIVE", None)
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
    TENANT = os.environ.get("TENANT", None)
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN", None)

    # Google Drive details
    PROJECT_ID_GDRIVE = os.environ.get("PROJECT_ID_GDRIVE", None)
    PRIVATE_KEY_GDRIVE = os.environ.get("PRIVATE_KEY_GDRIVE", None)
    PRIVATE_KEY_ID = os.environ.get("PRIVATE_KEY_ID", None)
    CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL", None)
    CLIENT_ID_GDRIVE = os.environ.get("CLIENT_ID_GDRIVE", None)
    CLIENT_X509_CERT_URL = os.environ.get("CLIENT_X509_CERT_URL", None)

    # Mongo DB
    MONGO_URL = os.environ.get("MONGO_URL", None)
    DB_NAME = os.environ.get("DB_NAME", None)

else:
    #Config File
    config_file = "config.ini"
    config = ConfigParser()
    raw_config = RawConfigParser()
    config.read(config_file)
    raw_config.read(config_file)

    # Pyrogram details
    API_ID = config.get(NAME, 'API_ID')
    API_HASH = config.get(NAME, "API_HASH")
    BOT_TOKEN = config.get(NAME, "BOT_TOKEN")

    # OneDrive details
    CLIENT_ID_ONEDRIVE = config.get(NAME, "CLIENT_ID_ONEDRIVE")
    CLIENT_SECRET = config.get(NAME, "CLIENT_SECRET")
    TENANT = config.get(NAME, "TENANT")
    REFRESH_TOKEN = config.get(NAME, "REFRESH_TOKEN")

    # Google Drive details
    PROJECT_ID_GDRIVE = config.get(NAME, "PROJECT_ID_GDRIVE")
    PRIVATE_KEY_GDRIVE = config.get(NAME, "PRIVATE_KEY_GDRIVE")
    PRIVATE_KEY_ID = config.get(NAME, "PRIVATE_KEY_ID")
    CLIENT_EMAIL = config.get(NAME, "CLIENT_EMAIL")
    CLIENT_ID_GDRIVE = config.get(NAME, "CLIENT_ID_GDRIVE")
    CLIENT_X509_CERT_URL = raw_config.get(NAME, "CLIENT_X509_CERT_URL")

    # Mongo DB
    MONGO_URL = config.get(NAME, "MONGO_URL")
    DB_NAME = config.get(NAME, "DB_NAME")

logger.debug("Env set properly")