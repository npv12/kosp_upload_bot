from abc import ABC, abstractmethod


class DocumentProccesor(ABC):
    """Base abstract class for downloading and uploading of all the files from the server.
    This class defines the bare amount of functions all the downloaders must have.
    Methods
        download: Downloads the file from the given url and stores it in a temporary location
        upload: Uploads the given file to gdrive. The file is deleted after the upload.
    """

    def download(self, url: str, message) -> str:
        """Downloads the file from the given url and stores it in a temporary location.
        Args:
            url: The url of the file to be downloaded.
            message: The message to edit to show the progress of the download.
        """
        pass

    def upload(self, file_path: str) -> bool:
        """Uploads the given file to gdrive. The file is deleted after the upload.
        Args:
            file_path: The path of the file to be uploaded.
            folder_id: The id of the folder where the file will be uploaded.
        """
        pass