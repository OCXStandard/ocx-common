#  Copyright (c) 2023-2024. #  OCX Consortium https://3docx.org. See the LICENSE
"""Shared utility classes and functions"""

# System imports
import errno
import os
import re
import sys
import urllib.parse
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from typing import Dict, Generator, List


# Third party imports

# Project imports


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


def is_valid_windows_path(path: str) -> bool:
    windows_pattern = re.compile(
        r"^(?:(?:[a-zA-Z]:\\|\\\\[^\\/:*?\"<>|\r\n]+\\[^\\/:*?\"<>|\r\n]+)|"
        r"(?:(?:\.\.?\\)*[^\\/:*?\"<>|\r\n]+\\?)*)(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*$"
    )
    return bool(windows_pattern.match(path))


def is_valid_file_uri(uri: str) -> bool:
    """
    Validate whether the given URI is a correctly formatted file:// URI.
        Ensures file:// scheme is present (urllib.parse.urlparse(uri).scheme == "file").
        Handles Windows paths correctly, including:
        file://C:/path.txt
        file:///C:/path.txt
        file://localhost/C:/path.txt
        Handles Unix paths correctly, ensuring / is present.

    Args:
        uri (str): The file URI to check.

    Returns:
        bool: True if the URI is correctly formatted, False otherwise.
    """

    parsed = urllib.parse.urlparse(uri)

    # Must start with "file://"
    if not uri.startswith("file://"):
        return False

    # Ensure netloc is empty or 'localhost' (except for Windows drive letters)
    if parsed.netloc and parsed.netloc != "localhost":
        # Windows paths might store drive letters in netloc
        if not re.match(r"^[A-Za-z]:/.*", parsed.netloc + parsed.path):
            return False

    # Reject incorrect Windows drive formats (e.g., `C|/`)
    if re.match(r"^/[A-Za-z]\|/", parsed.path):
        return False

    # Windows absolute path: `/C:/path.txt` or `C:/path.txt` in netloc
    windows_pattern = r"^/[A-Za-z]:/.*"

    # Unix absolute path: `/home/user/file.txt` (must start with single `/`)
    unix_pattern = r"^/[^/].*"

    return bool(
        re.match(windows_pattern, parsed.path) or re.match(unix_pattern, parsed.path)
    )


def is_uri(uri) -> bool:
    """Return True if source is an uri, False otherwise"""
    if "file:" in uri or "http" in uri:
        return True
    else:
        return False


def is_file_uri(uri) -> bool:
    """Return True if source is a file uri, False otherwise"""
    if "file" in uri:
        return True
    else:
        return False


def file_uri_to_path(uri: str) -> str:
    """Converts a file:// URI to a proper file system path."""
    if "file" in uri:
        parsed = urllib.parse.urlparse(uri)

        # Handle Windows UNC paths (file://server/share/file.txt → \\server\share\file.txt)
        if parsed.netloc:
            file_path = f"\\\\{parsed.netloc}{parsed.path}"
        else:
            file_path = parsed.path

        # Strip leading slash for Windows drive letters (e.g., /C:/path → C:/path)
        if (
            os.name == "nt"
            and file_path.startswith("/")
            and len(file_path) > 2
            and file_path[2] == ":"
        ):
            file_path = file_path[1:]

        # Normalize for the OS (Windows backslashes, Unix forward slashes)
        return os.path.normpath(file_path)
    else:
        raise ValueError(f"{uri} is not a valid file uri")


def is_directory(source: str) -> bool:
    """Return True if the source is a directory, False otherwise"""
    return Path(source).is_dir()


def iter_files(directory: str, filter_str: str) -> Generator:
    """
    Iterate over files in a directory based on a specified filter pattern.

    Args:
        directory (str): The path to the directory.
        filter_str (str): The filter pattern to apply when filtering files.

    Returns:
        Generator: A generator yielding file paths that match the filter criteria.

    """
    if is_directory(directory):
        # Specify the folder path
        folder_path = Path(directory)
        # Using glob to filter files based on a pattern
        return folder_path.glob(filter_str)
