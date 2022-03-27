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
            res = httpx.get(url)
            content_length = int(res.headers['Content-Length'])

            data = b''

            for chunk in res.iter_bytes(chunk_size=1024 * 1024 * 10):
                if (chunk):
                    data += chunk
                progress: int = round(len(data) / content_length * 100, 2)
                print(progress)

            binary_file = open(local_filename, "wb")
            binary_file.write(data)
            binary_file.close()

            await self.message.edit_text("Downloaded successfully")
            return local_filename

        except:
            await self.message.edit_text("Download failed")
        return None
