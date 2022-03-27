import httpx
from bot.document_processor.base import DocumentProccesor
import os


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
                    for chunk in response.iter_bytes():
                        data += chunk
                        await self.__update_download_status__(
                            response.num_bytes_downloaded, total)
                        print(response.num_bytes_downloaded / total) * 100

            except:
                await self.message.edit_text("Failed to download the file")
            return local_filename

        except:
            await self.message.edit_text("Download failed")
        return None

    def __update_download_status__(self, progress: int, total: int):
        print(progress / total * 100)
        content: str = f"Downloading file ${progress/total*100}"
        try:
            self.message.edit_text(content)
        except:
            print(content)
