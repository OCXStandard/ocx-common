#  Copyright (c) 2025. #  OCX Consortium https://3docx.org. See the LICENSE


from pathlib import Path

from ocx_common.utilities import utilities


class SourceError(ValueError):
    """SourceValidator errors."""


class SourceValidator:
    """Methods for validating the existence and correctness of a data source on different fortmats."""

    @classmethod
    def validate(cls, source: str) -> str:
        """
        Validate the correctness AND existence of the data source.
        Args:
            source: The source file path or uri.

        Returns:
            Returns the valid uri or full Windows path if the source is valid.
        Raises:
              Raises a source error if source does not exist or the uri has a wrong syntax.
        """
        # The source is an uri
        try:
            if utilities.is_file_uri(source):
                file_path = utilities.get_uri_file_path(source)
                return str(Path(file_path).resolve())
            else:
                return str(Path(source).resolve())
        except ValueError as e:
            raise SourceError(
                f"The source is not a correct formatted uri: {source}. Error {e}"
            ) from e
