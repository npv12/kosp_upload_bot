from bot.document_processor.base import DocumentProccesor
import requests
import os


class DirectLink(DocumentProccesor):

    async def download(self, url: str, message) -> str:

        temp_folder_path: str = "./DumpsterFire/"

        try:

            if not os.path.exists(temp_folder_path):
                os.mkdir(temp_folder_path)

            local_filename: str = temp_folder_path + url.split('/')[-1]
            res = requests.get(url, stream=True, allow_redirects=True)
            content_length = int(res.headers['Content-Length'])

            data = b''

            for chunk in res.iter_content(chunk_size=1024 * 1024 * 10):
                if (chunk):
                    data += chunk
                progress: int = round(len(data) / content_length * 100, 2)
                print(progress)

            await message.edit_text("Downloaded successfully")
            return local_filename

        except:
            await message.edit_text("Download failed")
        return None
