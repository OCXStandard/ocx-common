#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE


# Project imports

from .conftest import TEST_MODEL
from ocx_common.parser.parsers import OcxParser
from ocx_common.x_path.x_path import OcxGuidRef, OcxPath


def test_find_vessel(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    xpath = 'ocx:Vessel'
    ocx_path = OcxPath(root, namespaces=root.nsmap)
    node = ocx_path.find(xpath)
    assert len(node) == 1


def test_find_all_guids(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    guids = OcxGuidRef(root, namespaces=root.nsmap).get_all_guids()
    assert len(guids) == 25


def test_find_child_guids(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()

    guids = OcxGuidRef(root, namespaces=root.nsmap).get_child_guids('CoordinateSystem')
    assert len(guids) == 25


def test_get_all_named_nodes(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    nodes = OcxPath(root, namespaces=root.nsmap).get_all_named_ocx_elements('CoordinateSystem')
    assert len(nodes) == 1
