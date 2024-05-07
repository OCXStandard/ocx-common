#  Copyright (c) 2024. OCX Consortium https://3docx.org. See the LICENSE

import os
import sys

from loguru import logger

# To make sure that the tests import the modules this has to come before the import statements
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

logger.disable("ocx_common")

SCHEMA_VERSION = '3.0.0rc3'
NAMESPACE = "https://3docx.org/fileadmin//ocx_schema//V300rc3//OCX_Schema.xsd"
MODEL1 = 'NAPA-OCX_M1_v300rc3.3docx'

TEST_MODEL = MODEL1
