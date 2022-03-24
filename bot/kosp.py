from configparser import ConfigParser
from bot import API_ID, API_HASH, BOT_TOKEN
from pyrogram import Client

from . import __version__


class KOSP(Client):

    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = "config.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root="bot/plugins")
        super().__init__(
            session_name=name,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            app_version=f"KOSP v{__version__}",
            workdir=".",
            config_file=config_file,
            workers=8,
            plugins=plugins,
        )

    def start(self):
        super().start()
        print(f"KOSP is running. Version is v{__version__}")

    def stop(self):
        super().stop()
        print("I am off to sleep now")