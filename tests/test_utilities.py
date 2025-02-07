#  Copyright (c) 2024. OCX Consortium https://3docx.org. See the LICENSE

from pathlib import Path

# Project import
from ocx_common.utilities.utilities import (
    is_substring_in_list,
    OcxXml,
    parent_directory,
    all_equal,
    camel_case_split,
    dromedary_case_split,
    list_files_in_directory,
    resource_path,
    get_file_path,
    SourceValidator,
    SourceError,
)

from .conftest import TEST_MODEL, SCHEMA_VERSION, NAMESPACE


class TestOcxXml:
    def test_get_version(self, shared_datadir):
        model = shared_datadir / TEST_MODEL
        assert OcxXml.get_version(str(model.resolve())) == SCHEMA_VERSION

    def test_get_ocx_namespace(self, shared_datadir):
        model = shared_datadir / TEST_MODEL
        assert OcxXml.get_ocx_namespace(str(model.resolve())) == NAMESPACE

    def test_get_all_namespaces(self, shared_datadir, data_regression):
        model = shared_datadir / TEST_MODEL
        result = OcxXml.get_all_namespaces(str(model.resolve()))
        data_regression.check(result)

    def test_has_ocx_namespace(self, shared_datadir):
        model = shared_datadir / TEST_MODEL
        assert OcxXml.has_ocx_namespace(str(model.resolve())) == True

    def test_has_unitsml_namespace(self, shared_datadir):
        model = shared_datadir / TEST_MODEL
        assert OcxXml.has_unitsml_namespace(str(model.resolve())) == True


def test_is_substring_in_list_1():
    assert is_substring_in_list(
        "Doe", ["John Doe", "Alicia", "Hello world", "package.file"]
    )


def test_is_substring_in_list_2():
    assert is_substring_in_list(
        ".file", ["John Doe", "Alicia", "Hello world", "package.file"]
    )


def test_is_substring_in_list_3():
    assert not is_substring_in_list(
        "Help", ["John Doe", "Alicia", "Hello world", "package.file"]
    )


def test_parent_directory(shared_datadir):
    file = shared_datadir / TEST_MODEL
    assert parent_directory(str(file.resolve())) == str(shared_datadir.resolve())


def test_all_equal_1():
    assert all_equal(["John", "John", "John", "John", "John", "John", "John"])


def test_all_equal_2():
    assert not all_equal(["John", "Alice", "John", "John", "John", "John", "John"])


def test_camel_case_split():
    assert camel_case_split("CamelCase") == ["Camel", "Case"]


def test_dromedary_case_split():
    assert dromedary_case_split("dromedaryCase") == ["dromedary", "Case"]


def test_list_files_in_directory(shared_datadir):
    assert list_files_in_directory(shared_datadir, "*.3docx") == [TEST_MODEL]


class TestSourceValidator:
    def test_validate(self, shared_datadir):
        file = shared_datadir / TEST_MODEL
        assert SourceValidator.exists(str(file.resolve()))

    def test_validate_url(self):
        url = "https://3docx.org/fileadmin//ocx_schema//V300//OCX_Schema.xsd"
        assert SourceValidator.exists(url)

    def test_validate_invalid_url(self):
        url = "https:/fileadmin//ocx_schema//V300//OCX_Schema.xsd"
        assert SourceValidator.is_valid_uri(url) is False
    def test_is_url_1(self):
        assert SourceValidator.is_valid_uri("https://google.com")

    def test_is_url_2(self):
        assert SourceValidator.is_valid_uri("http://server.localhost")

    def test_is_url_3(self):
        assert SourceValidator.is_valid_uri("file://./OCX_Schema.xsd")

    def test_is_directory(self, shared_datadir):
        assert SourceValidator.is_directory(shared_datadir)

    def test_mkdir(self, shared_datadir):
        directory = SourceValidator.mkdir("test_folder")
        assert Path(directory).exists()

    def test_filter_files(self, shared_datadir):
        files = SourceValidator.filter_files(str(shared_datadir.resolve()), "*.3docx")
        assert len(list(files)) == 1


def test_resource_path(shared_datadir):
    file = Path.joinpath(shared_datadir, TEST_MODEL)
    path = resource_path(str(file))
    assert path == str(file)


def test_get_file_path(shared_datadir):
    file = Path.joinpath(shared_datadir, TEST_MODEL)
    path = get_file_path(str(file))
    assert path == str(file)
