from configparser import ConfigParser

from pyrogram import Client

from bot import API_ID, API_HASH, BOT_TOKEN
from bot.utils.logging import logger

from . import __version__


class Flamingo(Client):

    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = "config.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root="bot/plugins")
        super().__init__(
            name=name,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            app_version=f"Flamingo v{__version__}",
            workdir=".",
            workers=8,
            plugins=plugins,
        )

    def start(self):
        super().start()
        logger.info(f"Flamingo is running. Version is v{__version__}")

    def stop(self):
        super().stop()
        logger.info("I am off to sleep now")