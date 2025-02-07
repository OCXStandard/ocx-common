#  Copyright (c) 2023-2024. #  OCX Consortium https://3docx.org. See the LICENSE
"""Shared utility classes and functions"""

# System imports
import errno
import os
import re
import sys
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from typing import Dict, Generator, List
from urllib.parse import urlparse


class SourceError(ValueError):
    """SourceValidator errors."""


def is_substring_in_list(substring, string_list):
    """

    Args:
        substring: The search string
        string_list: List of strings

    Returns:
        True if the substring is found, False otherwise.
    """
    return any(substring in string for string in string_list)


def all_equal(iterable) -> True:
    """
    Verify that all items in a list are equal
    Args:
        iterable:

    Returns:
        True if all are equal, False otherwise.
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(".."))
    return os.path.join(base_path, relative_path)


def parent_directory(file: str) -> str:
    """The full path to the folder containing the ``file``

    Args:
        file: The name of an existing file
    """
    return os.path.realpath(os.path.join(os.path.dirname(file), ""))


def nested_dict():
    """
    A recursive function that creates a default dictionary where each value is
    another default dictionary.
    """
    return defaultdict(nested_dict)


def get_key_from_value(my_dict, value):
    for key, val in my_dict.items():
        if val == value:
            return key
    return None  # Return None if the value is not found


def default_to_regular(d) -> Dict:
    """
    Converts defaultdicts of defaultdicts to dict of dicts.

    Args:
        d: The dict to be converted

    """
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def default_to_grid(d) -> Dict:
    """
    Converts defaultdicts to a data grid with unique row ids.

    Args:
        d: The dict to be converted

    """
    if isinstance(d, defaultdict):
        print(d.items())
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def list_files_in_directory(directory: str, filter: str) -> List:
    """
    Lists files in a directory based on a specified filter using glob pattern matching.

    Args:
        directory (str): The path to the directory.
        filter (str): The filter pattern to apply when listing files.

    Returns:
        List: A list of file paths that match the filter criteria.
    Raises:
        AssertionError: If the directory does not exist.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise AssertionError(errno.EEXIST)
    return [file.name for file in dir_path.glob(filter) if file.is_file()]


def camel_case_split(str) -> List:
    """Split camel case string to individual strings."""
    return re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", str)


def dromedary_case_split(str) -> List:
    """Split camel case string to individual strings."""
    return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", str)


def get_file_path(file_name):
    """Get the correct file path also when called within a one-file executable."""
    base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.abspath("..")
    return os.path.join(base_path, file_name)


class SourceValidator:
    """Methods for validating the existence and correctness of a data source."""

    @staticmethod
    def exists(source: str) -> str:
        """
        Validate the existence of a data source.

        Args:
            source: The source file path or url.

        Returns:
            Returns the uri or full path if the source is valid.
        Raises:
              Raises a source error if source does not exist.
        """
        # Url
        if "http" in source:
            parsed_url = urlparse(source)
            if bool(parsed_url.scheme and parsed_url.netloc):
                return parsed_url.geturl()
            else:
                raise SourceError(f"(The {source} is not a valid url.")
        # File
        else:
            file_path = Path(source)
            if file_path.exists():
                return str(file_path.resolve())
            else:
                raise SourceError(f"The {source} does not exist.")

    @staticmethod
    def is_valid_uri(uri: str) -> bool:
        """Return true if uri ``source`` is a valid url."""
        try:
            parsed = urlparse(uri)
            # A valid URI must have a scheme
            if not parsed.scheme:
                return False

            # Special case for 'file:' scheme (netloc may be empty)
            if parsed.scheme == "file":
                return bool(parsed.path)

            # For other schemes, both scheme and netloc must be present
            return bool(parsed.netloc)
        except ValueError:
            return False

    @staticmethod
    def is_directory(source: str) -> bool:
        """Return True if the source is a directory, False otherwise"""
        return Path(source).is_dir()

    @staticmethod
    def mkdir(source: str) -> str:
        """Create the directory and any parent folders if missing.

        Args:
            source: The folder name

        Returns:
            The folder name
        """
        folder = Path(source)
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        return source

    @staticmethod
    def filter_files(directory: str, filter_str: str) -> Generator:
        """
        Filters files in a directory based on a specified filter pattern.

        Args:
            directory (str): The path to the directory.
            filter_str (str): The filter pattern to apply when filtering files.

        Returns:
            Generator: A generator yielding file paths that match the filter criteria.
        """
        if SourceValidator.is_directory(directory):
            # Specify the folder path
            folder_path = Path(directory)
            # Using glob to filter files based on a pattern
            return folder_path.glob(filter_str)


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
            ocx_model = Path(SourceValidator.exists(model))
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
