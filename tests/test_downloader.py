#  Copyright (c) 2023-2025. OCX Consortium https://3docx.org. See the LICENSE

from pathlib import Path
import shutil
from tests.conftest import NAMESPACE
from ocx_common.utilities.downloader import SchemaDownloader

temp = Path("./temp")


def test_download_from_url():
    """Test download from external source."""
    if not temp.exists():
        temp.mkdir(parents=True)
    downloader = SchemaDownloader(temp)
    downloader.wget(NAMESPACE)
    files = list(temp.glob("*.xsd"))
    assert len(files) == 3
    # Clean up
    if temp.exists():
        shutil.rmtree(temp)


def test_download_from_file(shared_datadir: Path):
    """Test download from a local file."""
    temp = shared_datadir / "temp"
    if not temp.exists():
        temp.mkdir(parents=True)
    downloader = SchemaDownloader(temp)
    ocx_schema = shared_datadir / "OCX_Schema.xsd"
    downloader.wget(str(ocx_schema.resolve()))
    files = list(temp.glob("*.xsd"))
    assert len(files) == 3
    # Clean up
    if temp.exists():
        shutil.rmtree(temp)
