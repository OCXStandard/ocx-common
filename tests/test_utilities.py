#  Copyright (c) 2024. OCX Consortium https://3docx.org. See the LICENSE

from pathlib import Path
import pytest

# Project import
from ocx_common.utilities import utilities

from .conftest import TEST_MODEL, MODEL_FOLDER


def test_is_substring_in_list_1():
    assert utilities.is_substring_in_list(
        "Doe", ["John Doe", "Alicia", "Hello world", "package.file"]
    )


def test_is_substring_in_list_2():
    assert utilities.is_substring_in_list(
        ".file", ["John Doe", "Alicia", "Hello world", "package.file"]
    )


def test_is_substring_in_list_3():
    assert not utilities.is_substring_in_list(
        "Help", ["John Doe", "Alicia", "Hello world", "package.file"]
    )


def test_parent_directory(shared_datadir):
    file = shared_datadir / TEST_MODEL
    assert utilities.parent_directory(str(file.resolve())) == str(shared_datadir.resolve())


def test_all_equal_1():
    assert utilities.all_equal(["John", "John", "John", "John", "John", "John", "John"])


def test_all_equal_2():
    assert not utilities.all_equal(["John", "Alice", "John", "John", "John", "John", "John"])


def test_camel_case_split():
    assert utilities.camel_case_split("CamelCase") == ["Camel", "Case"]


def test_dromedary_case_split():
    assert utilities.dromedary_case_split("dromedaryCase") == ["dromedary", "Case"]


def test_list_files_in_directory(shared_datadir):
    folder = shared_datadir / MODEL_FOLDER
    assert utilities.list_files_in_directory(folder, "*.3docx") == [TEST_MODEL]


def test_resource_path(shared_datadir):
    file = Path.joinpath(shared_datadir, TEST_MODEL)
    path = utilities.resource_path(str(file))
    assert path == str(file)


def test_get_file_path(shared_datadir):
    file = Path.joinpath(shared_datadir, TEST_MODEL)
    path = utilities.get_file_path(str(file))
    assert path == str(file)


def test_is_directory(shared_datadir):
    assert utilities.is_directory(shared_datadir)


def test_is_directory_false(shared_datadir):
    not_exist = shared_datadir / "not_exist"
    assert utilities.is_directory(not_exist) is False


def test_is_valid_windows_path_1():
    assert utilities.is_valid_windows_path("C:\\Users\\oca\\OneDrive - DNV\\Git_Repos\\TestModels\\Latest")


# @pytest.mark.parametrize(
#     "uri, expected",
#     [
#         ("file://C:/Users/test/file.txt", True),  # ✅ Valid Windows absolute path
#         ("file:///C:/absolute/windows/path.txt", True),  # ✅ Windows absolute path with triple slashes
#         ("file://localhost/C:/path.txt", True),  # ✅ Windows localhost path
#         ("file:///home/user/file.txt", True),  # ✅ Unix absolute path
#         ("file:/relative/path.txt", False),  # ❌ Missing slashes
#         ("file://C|/invalid/path.txt", False),  # ❌ Incorrect Windows drive format
#         ("file://C:/valid/path.txt", True),  # ✅ Valid Windows absolute path
#         ("file:\\backslashes\\wrong.txt", False),  # ❌ Backslashes are not allowed
#         ("http://example.com/file.txt", False),  # ❌ Wrong scheme
#     ],
# )
# def test_file_uri_format(uri, expected):
#     """Test if file URIs are formatted correctly."""
#     assert utilities.is_valid_file_uri(uri) == expected

def test_file_uri_to_path(uri, expected):
    assert utilities.file_uri_to_path(uri) == expected

def test_file_uri_to_path_1():
    assert utilities.file_uri_to_path("file:C:/User/john/myfile.txt") == "C:\\User\\john\\myfile.txt"

def test_file_uri_to_path_2():
    assert utilities.file_uri_to_path("file:///C:/User/john/myfile.txt") == "C:\\User\\john\\myfile.txt"

def test_file_uri_to_path_3():
    assert utilities.file_uri_to_path("file://server/share/myfile.txt") == "server\\share\\myfile.txt"

def test_file_uri_to_path_4():
    assert utilities.file_uri_to_path("file:///home/user/myfile.txt") == "/home/user/myfile.txt"
