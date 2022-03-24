from abc import ABC, abstractmethod
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class DocumentProccesor(ABC):
    """Base abstract class for downloading and uploading of all the files from the server.
    This class defines the bare amount of functions all the downloaders must have.
    Methods
        download: Downloads the file from the given url and stores it in a temporary location
        upload: Uploads the given file to gdrive. The file is deleted after the upload.
    """

    abstractmethod

    async def download(self, url: str, message) -> str:
        """Downloads the file from the given url and stores it in a temporary location.
        Args:
            url: The url of the file to be downloaded.
            message: The message to edit to show the progress of the download.
        """
        pass

    async def upload(self, file_name: str, message) -> bool:
        """Uploads the given file to gdrive. The file is deleted after the upload.
        Args:
            file_path: The path of the file to be uploaded.
            folder_id: The id of the folder where the file will be uploaded.
        """

        gauth = GoogleAuth()

        drive = GoogleDrive(gauth)
        gauth.LoadCredentials()

        file1 = drive.CreateFile({
            'title': 'upload success.txt'
        })  # Create GoogleDriveFile instance with title 'Hello.txt'.
        file1.SetContentString(
            'Hello World!')  # Set content of the file from given string.
        file1.Upload()

        print("Upload one complete")

        file2 = drive.CreateFile({'title': 'boot.img'})
        file2.SetContentFile(file_name)
        file2.Upload()