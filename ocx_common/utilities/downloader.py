#  Copyright (c) 2023-2025. OCX Consortium https://3docx.org. See the LICENSE
from pathlib import Path
from typing import Optional
from loguru import logger

# Third part imports
from xsdata.utils.downloader import Downloader
from xsdata.codegen import opener


# Module imports
from ocx_common.utilities.utilities import SourceValidator


class SchemaDownloader(Downloader):
    """Downloader specialisation class.

    Arguments:
        output: The location of the download folder relative to current directory

    Args:
        folder: The download target folder.
    Properties:
        schema_folder: The path to the schema download folder
    """

    def __init__(self, folder: Path):
        super().__init__(folder)
        self.schema_folder = folder

    def write_file(self, uri: str, location: Optional[str], content: str):
        """
        Override super class method and output all schemas into one folder.

        Arguments:
            content: The schema content.
            location: The download location.
            uri: the download target resource. All referenced schemas will be collected.
        """
        # Get the uri file name
        name = Path(uri).name
        file_path = self.schema_folder / name
        file_path.write_text(content, encoding="utf-8")
        logger.debug(
            f"Writing schema {file_path.resolve()} to folder {self.schema_folder.resolve()}"
        )
        # logger.debug(content)
        self.downloaded[uri] = file_path

        if location:
            self.downloaded[location] = file_path

    def wget(self, uri: str, location: Optional[str] = None):
        """Download handler for any uri input with circular protection.
        Override super class method to handle a local file.

        """
        try:
            if SourceValidator.is_valid_uri(uri):
                if not (
                    uri in self.downloaded or (location and location in self.downloaded)
                ):
                    self.downloaded[uri] = None
                    self.downloaded[location] = None
                    self.adjust_base_path(uri)

                    logger.info(f"Fetching {uri}")

                    input_stream = opener.open(uri).read()  # nosec
            else:
                input_file = Path(uri).resolve()
                with open(str(input_file), "rb") as file:
                    input_stream = file.read()
            if uri.endswith("wsdl"):
                self.parse_definitions(uri, input_stream)
            else:
                self.parse_schema(uri, input_stream)

                self.write_file(uri, location, input_stream.decode())

        except FileNotFoundError:
            print(f"The file at {uri} was not found.")

        except Exception as e:
            print(f"An error occurred: {e}")
