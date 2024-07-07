#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE

# Third party imports
from lxml import etree

# Project imports
from .conftest import TEST_MODEL, SCHEMA_VERSION
from ocx_common.parser.parsers import OcxParser
from ocx_common.x_path.x_path import OcxPathBuilder
from ocx_common.x_path.xelement import LxmlElement


def test_select_all_named_nodes(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    search = etree.XPath(path=OcxPathBuilder.select_all_named_nodes('RefPlane'),
                         namespaces=root.nsmap)
    result = search(root)
    assert len(result) == 13


def test_select_current_node(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    search = etree.XPath(path=OcxPathBuilder.select_current_node(),
                         namespaces=root.nsmap)
    result = search(root)
    node = result[0]
    assert node.get('schemaVersion') == SCHEMA_VERSION


def test_select_parent_node(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    panel = LxmlElement.find_child_with_name(root, 'Panel')
    search = etree.XPath(path=OcxPathBuilder.select_parent_node(),
                         namespaces=root.nsmap)
    result = search(panel)
    parent = result[0]
    assert parent.get('id') == 'nplcid1'


def test_select_named_parent_node(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    panel = LxmlElement.find_child_with_name(root, 'XRefPlanes')
    search = etree.XPath(path=OcxPathBuilder.select_named_parent_node(parent='CoordinateSystem'),
                         namespaces=root.nsmap)
    result = search(panel)
    parent = result[0]
    assert parent.get('id') == 'nplcid7'


def test_select_all_nodes_with_attributes_name(shared_datadir):
    file = shared_datadir / TEST_MODEL
    parser = OcxParser(str(file))
    root = parser.get_root()
    search = etree.XPath(path=OcxPathBuilder.select_nodes_with_attributes_name('functionType'),
                         namespaces=root.nsmap)
    result = search(root)
    assert len(result) == 1


def test_select_all_children_with_attribute_name(shared_datadir):
    assert False
