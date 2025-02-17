#  Copyright (c) 2025. #  OCX Consortium https://3docx.org. See the LICENSE
from pathlib import Path
import pytest
from ocx_common.utilities.source_validator import SourceValidator
from tests.conftest import TEST_MODEL, MODEL_FOLDER


def test_validate_1(shared_datadir):
    uri = shared_datadir / MODEL_FOLDER / TEST_MODEL
    file_location = SourceValidator.validate(str(uri))
    assert uri.resolve() == Path(file_location).resolve()

@pytest.mark.parametrize(
    "uri, expected",
    [
        ("file://C:/Users/test/file.txt", "C:/Users/test/file.txt"),  # ✅ Valid Windows absolute path
        ("file:///C:/absolute/windows/path.txt", True),  # ✅ Windows absolute path with triple slashes
        ("file://localhost/C:/path.txt", True),  # ✅ Windows localhost path
        ("file:///home/user/file.txt", True),  # ✅ Unix absolute path
        ("file:/relative/path.txt", False),  # ❌ Missing slashes
        ("file://C|/invalid/path.txt", False),  # ❌ Incorrect Windows drive format
        ("file://C:/valid/path.txt", True),  # ✅ Valid Windows absolute path
        ("file:\\backslashes\\wrong.txt", False),  # ❌ Backslashes are not allowed
        ("http://example.com/file.txt", False),  # ❌ Wrong scheme
    ],
)
def test_validate(uri, expected):
    assert SourceValidator.validate(uri) == expected
