#  Copyright (c) 2025. #  OCX Consortium https://3docx.org. See the LICENSE
import re
from pathlib import Path
from typing import Dict

from ocx_common.utilities.source_validator import SourceError, SourceValidator


class OcxXml:
    """Find the schema version of an 3Docx XML model."""

    @staticmethod
    def get_version(model: str) -> str:
        """
        The schema version of the model.
        Args:
            model: The source file path or uri

        Returns:
            The schema version of the 3Docx XML model.
        """
        try:
            version = "NA"
            ocx_model = Path(SourceValidator.validate(model))
            content = ocx_model.read_text().split()
            for item in content:
                if "schemaVersion" in item:
                    version = item[item.find("=") + 2 : -1]
            return version
        except SourceError as e:
            raise SourceError(e) from e

    @staticmethod
    def get_ocx_namespace(model: str) -> str:
        """Return the OCX schema namespace of the model.

        Args:
            model: The source path or uri

        Returns:
              The OCX schema namespace of the model.
        """
        namespace = "NA"
        ocx_model = Path(model).resolve()
        if OcxXml.has_ocx_namespace(str(ocx_model)):
            content = ocx_model.read_text().split()
            for item in content:
                if "xmlns:ocx" in item:
                    # Extract all characters between double quotes
                    namespace = re.findall(r'"(.*?)"', item)
                    namespace = namespace[0]
        return namespace

    @staticmethod
    def has_ocx_namespace(model: str) -> bool:
        """Return True if the OCX schema namespace is defined.

        Args:
            model: The source path or uri

        Returns:
              True if the xmlns:ocx is defined, False otherwise.
        """
        ocx_model = Path(model).resolve()
        content = ocx_model.read_text()
        return "xmlns:ocx" in content

    @staticmethod
    def has_unitsml_namespace(model: str) -> bool:
        """Return True if the OCX schema unitsml namespace is defined.

        Args:
            model: The source path or uri

        Returns:
              True if the xmlns:unitsml is defined, False otherwise.
        """
        ocx_model = Path(model).resolve()
        content = ocx_model.read_text()
        return "xmlns:unitsml" in content

    @staticmethod
    def get_all_namespaces(model: str) -> Dict:
        """Return all the xmlns namespace map defined in the 3Docx model.

        Args:
            model: The source path or uri

        Returns:
              The namespace mappings.
        """
        namespaces = {}
        ocx_model = Path(model).resolve()
        content = ocx_model.read_text().split()
        for item in content:
            if "xmlns:" in item:
                if match := re.search(r':([^=]+)="([^"]+)"', item):
                    prefix = match[1]
                    namespace = match[2]
                    namespaces[prefix] = namespace
        return namespaces
