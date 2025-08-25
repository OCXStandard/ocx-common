#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE


from lxml import etree

from ocx_common.lxml_wrapper.xelement import XsdElement

# Project imports
from ocx_common.ocx_query.query import OcxGuidRef, OcxPath, OcxPathBuilder


class TestOcxPath:

    def test_find_vessel(self, load_model_1):
        root = load_model_1.get_root()
        ocx_path = OcxPath(root, namespaces=root.nsmap)
        node = ocx_path.get_all_named_ocx_elements(name="Vessel", namespace="ocx")
        vessel = node[0]
        assert vessel.get("name") == "OCX-MODEL1/A"

    def test_find_vessel_guid(self, load_model_1):
        root = load_model_1.get_root()
        ns_map = load_model_1.get_namespaces()
        ocx_path = OcxPath(root, namespaces=root.nsmap)
        path = OcxPathBuilder.select_named_nodes_with_global_attribute_name("Vessel", attribute_name="GuidRef")
        search = etree.XPath(path=path,
                             namespaces=ns_map
                             )
        vessel = search(root)

        vessel = XsdElement.get_named_attribute(vessel, attribute_name="GUIDRef")
        assert guid == "7014a1ab-77c8-42ea-8322-e7a777da1327"

    def test_find_all_guids(self, load_model_1):
        root = load_model_1.get_root()
        guids = OcxGuidRef(root, namespaces=root.nsmap).get_all_guids()
        assert len(guids) == 25

    def test_find_child_guids(self, load_model_1):
        root = load_model_1.get_root()

        guids = OcxGuidRef(root, namespaces=root.nsmap).get_child_guids("CoordinateSystem")
        assert len(guids) == 25

    def test_get_all_named_nodes(self, load_model_1):
        root = load_model_1.get_root()
        nodes = OcxPath(root, namespaces=root.nsmap).get_all_named_ocx_elements(
            "CoordinateSystem"
        )
        assert len(nodes) == 1


class TestQuery:
    def test_get_all_guids(self, query_model_1):
        guids = query_model_1.get_global_guids()
        assert len(guids) == 25

    def test_get_vessel(self, query_model_1):
        vessel = query_model_1.get_vessel()
        assert vessel.get("name") == "OCX-MODEL1/A"


    def test_verify_references(self, query_model_1):
        query_model_1.verify_references()
