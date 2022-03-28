import httpx
import io
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

from bot import CLIENT_EMAIL, CLIENT_ID_GDRIVE, CLIENT_X509_CERT_URL, PRIVATE_KEY_GDRIVE, PRIVATE_KEY_ID, PROJECT_ID_GDRIVE
from bot.document_processor.base import DocumentProccesor

from bot.utils.progress import progress_callback

creds = {
    "type": "service_account",
    "project_id": PROJECT_ID_GDRIVE,
    "private_key_id": PRIVATE_KEY_ID,
    "private_key": PRIVATE_KEY_GDRIVE.replace("\\n", "\n"),
    "client_email": CLIENT_EMAIL,
    "client_id": CLIENT_ID_GDRIVE,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":
    "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": CLIENT_X509_CERT_URL
}


class GDrive(DocumentProccesor):

    async def download(self, url: str) -> str:

        temp_folder_path: str = "./DumpsterFire/"
        file_id = self.__parse_url__(url)

        credentials = service_account.Credentials.from_service_account_info(
            creds)
        drive_service = build('drive', 'v3', credentials=credentials)
        drive = drive_service.files()
        drive_file = drive.get(fileId=file_id, fields='name,size').execute()
        local_filename = temp_folder_path + drive_file['name']
        content_size = drive_file['size']

        download_request = drive.get_media(fileId=file_id)

        if not os.path.exists(temp_folder_path):
            os.mkdir(temp_folder_path)

        local_file = io.FileIO(local_filename,
                               'wb')  # this can be used to write to disk
        downloader = MediaIoBaseDownload(fd=local_file,
                                         request=download_request,
                                         chunksize=1024 * 1024 * 3)
        done = False
        print("Going to start download")
        while done is False:
            status, done = downloader.next_chunk()
            progress = status.progress() * content_size
            progress_callback(progress, content_size, self.message,
                              "Starting Download ....")
            print("Download %d%%." % int(status.progress() * 100))

        print("Completed")
        return local_filename

        try:

            pass

        except Exception as e:
            print(e)
            await self.message.edit_text("Download failed")
        return None

    def __parse_url__(self, url: str) -> str:
        url = url.replace("https://drive.google.com/file/d/", "")
        url = url.replace("/view?usp=sharing", "")
        return url