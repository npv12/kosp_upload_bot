from abc import ABC, abstractmethod
from typing import List
from graph_onedrive import OneDrive
from bot import CLIENT_ID, CLIENT_SECRET, TENANT, REFRESH_TOKEN

from bot.parser import parse_kosp


class DocumentProccesor(ABC):
    """Base abstract class for downloading and uploading of all the files from the server.
    This class defines the bare amount of functions all the downloaders must have.
    Methods
        download: Downloads the file from the given url and stores it in a temporary location
        upload: Uploads the given file to gdrive. The file is deleted after the upload.
    """

    message: any

    def __init__(self, message):
        self.message = message

    @abstractmethod
    async def download(self, url: str) -> str:
        """Downloads the file from the given url and stores it in a temporary location.
        Args:
            url: The url of the file to be downloaded.
            message: The message to edit to show the progress of the download.
        """
        pass

    async def upload(self, file_name: str) -> bool:
        """Uploads the given file to onedrive. The file is deleted after the upload.
        Args:
            file_path: The path of the file to be uploaded.
            folder_id: The id of the folder where the file will be uploaded.
        """

        # Upload path of the final file
        file_upload_path = parse_kosp(file_name)
        print(file_upload_path)

        # Use the context manager to manage a session instance
        my_drive = OneDrive(CLIENT_ID, CLIENT_SECRET, TENANT,
                            "http://localhost:8080", REFRESH_TOKEN)

        # Get the details of all the items in the root directory

        dir_to_travel: List[str] = file_upload_path.split("/")

        items = my_drive.list_directory()

        # Search through the root directory to find the file
        parent_folder_id = None
        dest_folder_id = None

        for folder in dir_to_travel:
            dest_folder_id = None
            for item in items:
                if "folder" in item and item.get("name") == folder:
                    dest_folder_id = item["id"]
                    break

            if dest_folder_id is None:
                dest_folder_id = my_drive.make_folder(folder, parent_folder_id)

            items = my_drive.list_directory(dest_folder_id)
            parent_folder_id = dest_folder_id

        # Upload the file
        new_file_id = await my_drive.upload_file(
            file_path=file_name,
            parent_folder_id=dest_folder_id,
            verbose=False,
            callback=self.__callback__)

        print("Upload complete")

    async def __callback__(self, progress: int, total: int):
        print(progress / total)
