import httpx
from bot.document_processor.base import DocumentProccesor
import os

from bot.utils.progress import progress_callback


class DirectLink(DocumentProccesor):

    async def download(self, url: str) -> str:

        temp_folder_path: str = "./DumpsterFire/"

        try:

            if not os.path.exists(temp_folder_path):
                os.mkdir(temp_folder_path)

            local_filename: str = temp_folder_path + url.split('/')[-1]
            data = b''

            try:

                with httpx.stream("GET", url) as response:
                    total = int(response.headers["Content-Length"])
                    for chunk in response.iter_bytes(chunk_size=1024 * 1024 *
                                                     10):
                        data += chunk
                        print(response.num_bytes_downloaded / total * 100)
                        await progress_callback(response.num_bytes_downloaded,
                                                total, self.message,
                                                "Downloading file...")

            except Exception as e:
                await self.message.edit_text("Failed to download the file")
                print(e)

            try:
                with open(local_filename, "wb") as f:
                    f.write(data)
            except:
                await self.message.edit_text("Failed to download the file")
                return False

            return local_filename

        except:
            await self.message.edit_text("Download failed")
        return None