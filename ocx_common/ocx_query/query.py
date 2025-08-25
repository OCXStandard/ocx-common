#  Copyright (c) 2025. #  OCX Consortium https://3docx.org. See the LICENSE
"""OCX model query"""

from enum import Enum
from typing import Any, Callable

from lxml import etree

from ocx_common.lxml_wrapper.xelement import XsdElement
from ocx_common.parser.xml_document_parser import LxmlParser
from ocx_common.x_path.x_path import OcxPathBuilder


def match_key_exclusive_value(d, match_key, exclude_value):
    # First, check if the match_key maps to the expected match_value
    # Then, ensure no *other* key maps to the exclude_value
    for k, v in d.items():
        if k != match_key and v == exclude_value:
            return False

    return True


class Ocx(Enum):
    VESSEL: str = "Vessel"
    PLATE: str = "Plate"
    BRACKET: str = "Bracket"
    STIFFENER: str = "Stiffener"
    PANEL: str = "Panel"
    GUIDREF: str = "GUIDRef"
    REFTYPE: str = "refType"


class OcxGuidRef:
    def __init__(
        self,
        element_node: etree.Element,
        namespaces: Any,
        extensions: Any = None,
        regexp: bool = True,
        smart_strings: bool = True,
    ):
        self._node = element_node
        self._namespaces = namespaces
        self._extensions = extensions
        self._regexp = regexp
        self._smart_strings = smart_strings

    def _get_guids(self, nodes: list) -> Any:
        guids = []
        for element in nodes:
            ns = etree.QName(element).namespace
            if element.get(f"{XsdElement.namespaces_decorate(ns)}refType") is None:
                guids.append(
                    element.get(f"{XsdElement.namespaces_decorate(ns)}GUIDRef")
                )
        return guids

    def get_all_guids(self) -> Callable:
        search = etree.XPath(
            path=OcxPathBuilder.select_any_nodes_with_global_attribute_name(
                attribute_name="GUIDRef"
            ),
            namespaces=self._namespaces,
            extensions=self._extensions,
            regexp=self._regexp,
            smart_strings=self._smart_strings,
        )
        nodes = search(self._node)
        return self._get_guids(nodes)

    def get_child_guids(self, node_name: str, namespace: str = "ocx") -> Callable:
        search = etree.XPath(
            path=OcxPathBuilder.select_any_nodes_with_global_attribute_name(
                attribute_name="GUIDRef"
            ),
            namespaces=self._namespaces,
            extensions=self._extensions,
            regexp=self._regexp,
            smart_strings=self._smart_strings,
        )
        nodes = search(self._node)
        return self._get_guids(nodes)


class OcxQuery:
    def __init__(self):
        self._parser = LxmlParser()

    def parse(self, ocx_model: str) -> bool:
        """Parse an OCX model"""
        return self._parser.parse(ocx_model, store_ids=True)

    def get_document_root(self) -> etree.Element:
        """Return the document root"""
        return self._parser.get_root()

    def namespaces(self) -> dict:
        return self._parser.get_namespaces()

    def get_vessel(self) -> etree.Element:
        root = self.get_document_root()
        ns_map = self.namespaces()
        path = OcxPathBuilder.select_all_named_nodes(nodename=Ocx.VESSEL.value)
        search = etree.XPath(path=path, namespaces=ns_map)
        vessel = search(root)
        if len(vessel) == 0:
            raise ValueError("The OCX model has no !rVessel element")
        return vessel[0]

    def get_global_guids(self) -> Callable[..., Any]:
        root = self.get_document_root()
        ns_map = self._parser.get_namespaces()
        return OcxGuidRef(root, namespaces=ns_map).get_all_guids()

    def verify_references(self) -> list[Any]:
        """Verify the references."""
        for element in self._parser.iter_elements():
            # print(f" {XsdElement.get_name(element)}")
            attrib = XsdElement.get_all_attributes(element)
            if match_key_exclusive_value(
                match_key=Ocx.GUIDREF.value,
                exclude_value=Ocx.REFTYPE.value,
                d=attrib,
            ):
                print(f"Got match!{element.tag}")
