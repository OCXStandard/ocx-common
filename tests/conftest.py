#  Copyright (c) 2024. OCX Consortium https://3docx.org. See the LICENSE

import os
import sys

import pytest
from icecream import ic
from loguru import logger

from ocx_common.ocx_query.query import OcxQuery

logger.enable("ocx_common")
# Project imports
from ocx_common.parser.xml_document_parser import LxmlParser

# Disable or enable debug/logging
ic.enable()
ic.configureOutput(includeContext=True, contextAbsPath=False)
logger.disable("ocx_common")

# To make sure that the tests import the modules this has to come before the import statements
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

SCHEMA_VERSION = "3.0.0"
NAMESPACE = "https://3docx.org/fileadmin//ocx_schema//V300//OCX_Schema.xsd"
MODEL1 = "NAPA-OCX_M1.3docx"
MODEL9 = "NAPA-OCX_M9.3docx"

MOCK_URL = "http://localhost:8080/rest/api"
MODEL_FOLDER = "models"
SCHEMA_FOLDER = "schemas"
TEST_MODEL = MODEL1

@pytest.fixture
def load_schema_from_file(shared_datadir) -> LxmlParser:
    """Load the schema from file and make it available for processing."""
    parser = LxmlParser()
    file = shared_datadir / SCHEMA_FOLDER / "OCX_Schema.xsd"
    parser.parse(file.absolute())
    assert parser.lxml_version() == (5, 3, 1, 0)
    return parser

@pytest.fixture
def load_model_1(shared_datadir) -> LxmlParser:
    """Load the schema from file and make it available for processing."""
    parser = LxmlParser()
    file = shared_datadir / MODEL_FOLDER / MODEL1
    parser.parse(file.absolute())
    assert parser.lxml_version() == (5, 3, 1, 0)
    return parser

@pytest.fixture
def load_model_9(shared_datadir) -> LxmlParser:
    """Load the schema from file and make it available for processing."""
    parser = LxmlParser()
    file = shared_datadir / MODEL_FOLDER / MODEL9
    parser.parse(file.absolute())
    assert parser.lxml_version() == (5, 3, 1, 0)
    return parser

@pytest.fixture
def query_model_1(shared_datadir) -> OcxQuery:
    """Load the model 1 from file."""
    query = OcxQuery()
    file = shared_datadir / MODEL_FOLDER / MODEL1
    query.parse(file.absolute())
    return query
