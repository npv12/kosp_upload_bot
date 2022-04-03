import httpx
from bot.constants import TEMP_FOLDER_PATH
from bot.document_processor.base import DocumentProccesor
import os
from bot.utils.parser import find_device

from bot.utils.progress import progress_callback
from bot.utils.logging import logger
from bot.database.maintainer_details import maintainer_details


class DirectLink(DocumentProccesor):

    async def download(self, user_id: int, url: str) -> str:

        if not os.path.exists(TEMP_FOLDER_PATH):
            os.mkdir(TEMP_FOLDER_PATH)

        logger.info("Downloading file from direct link")
        local_filename: str = url.split('/')[-1]
        device: str = find_device(local_filename)

        try:
            official_devices = maintainer_details.get_devices(user_id)
            if not official_devices:
                official_devices = []
            if device not in official_devices and not maintainer_details.is_admin(
                    user_id):
                logger.info("This user is not a maintainer of this device")
                raise Exception("INVALID_DEVICE")
        except:
            pass

        data = b''

        try:

            with httpx.stream("GET", url) as response:
                total = int(response.headers["Content-Length"])
                logger.info(f"The recieved file size is {total}")
                for chunk in response.iter_bytes(chunk_size=1024 * 1024 * 10):
                    data += chunk
                    logger.debug(response.num_bytes_downloaded / total * 100)
                    await progress_callback(response.num_bytes_downloaded,
                                            total, self.message,
                                            "Downloading file...")
                logger.info("Successfully downloaded the file")

        except Exception as e:
            logger.exception(e)

        try:
            logger.info(
                f"Trying to write the file to {TEMP_FOLDER_PATH}{local_filename}"
            )
            with open(TEMP_FOLDER_PATH + local_filename, "wb") as f:
                f.write(data)
        except:
            await self.message.edit_text("Failed to download the file")
            return False

        return local_filename