from bot.utils.logging import logger
from bot.document_processor.base import DocumentProccesor
from bot.document_processor.direct_link import DirectLink
from bot.document_processor.gdrive import GDrive


class DocumentProcessorFactory:

    @staticmethod
    def create_document_processor(url: str, message) -> DocumentProccesor:
        """The method which decides the concrete implementation
        to be used to process a particular file.
        This decision is made based on the url being provided.
        Parameters
            url: URL of the file to be downloaded.
        Returns
            object: The object of the concrete Document Processor class to be used
        """
        if "drive.google.com" in url:
            logger.info("The file is hosted on Google Drive")
            return GDrive(message)
        logger.info("The file is a direct link download")
        return DirectLink(message)