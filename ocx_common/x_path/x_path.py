#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE
"""A python XPath implementation for OCX types"""
# System imports
from typing import List, Any, Callable
from enum import Enum

# Third party imports
from lxml import etree
from lxml.etree import QName, XPathError

# Project imports
from ocx_common.x_path.xelement import LxmlElement


class OcxPathError(ValueError, XPathError):
    pass


class OcxPathBuilder:

    @staticmethod
    def select_all_named_nodes(nodename: str, namespace: str = 'ocx') -> str:
        return f'//{namespace}:{nodename}'

    @staticmethod
    def select_current_node() -> str:
        return '.'

    @staticmethod
    def select_parent_node() -> str:
        return 'parent::*'

    @staticmethod
    def select_named_parent_node(parent: str, namespace: str = 'ocx') -> str:
        return f'parent::{namespace}:{parent}'

    @staticmethod
    def select_nodes_with_attributes_name(attribute_name: str, namespace: str = 'ocx') -> str:
        return f'//{namespace}:*[@{namespace}:{attribute_name}]'

    @staticmethod
    def select_all_children_with_attribute_name(attribute_name: str, namespace: str = 'ocx') -> str:
        return f'//{namespace}:*[@{namespace}:{attribute_name}]'


class OcxPath:
    def __init__(self, document_root: etree.Element, namespaces: Any, extensions: Any = None,
                 regexp: bool = True, smart_strings: bool = True):
        self._root = document_root
        self._namespaces = namespaces
        self._extensions = extensions
        self._regexp = regexp
        self._smart_strings = smart_strings

    def get_ocx_attribute_value_collection(self, element: etree.Element, xpath: str,
                                           namespace: str = 'ocx') -> List[Any]:
        pass

    def get_all_named_ocx_elements(self, name: str, namespace: str = 'ocx') -> List[Any]:
        search = etree.XPath(path=OcxPathBuilder.select_all_named_nodes(name),
                             namespaces=self._namespaces,
                             regexp=self._regexp, smart_strings=self._smart_strings)
        return search(self._root)

    def get_all_named_children(self, node: etree.Element, child_name: str, namespace: str = 'ocx') -> List[Any]:
        search = etree.XPath(path=OcxPathBuilder.select_all_named_nodes(child_name),
                             namespaces=self._namespaces,
                             regexp=self._regexp, smart_strings=self._smart_strings)
        return search(self._root)


class OcxGuidRef:
    def __init__(self, element_node: etree.Element, namespaces: Any, extensions: Any = None,
                 regexp: bool = True, smart_strings: bool = True):
        self._node = element_node
        self._namespaces = namespaces
        self._extensions = extensions
        self._regexp = regexp
        self._smart_strings = smart_strings

    def _get_guids(self, nodes: List) -> Any:
        guids = []
        for element in nodes:
            ns = QName(element).namespace
            if element.get(f'{LxmlElement.namespaces_decorate(ns)}refType') is None:
                guids.append(element.get(f'{LxmlElement.namespaces_decorate(ns)}GUIDRef'))
        return guids

    def get_all_guids(self) -> Callable:
        search = etree.XPath(
            path=OcxPathBuilder.select_all_nodes_with_attributes_name(
                attribute_name='GUIDRef'),
            namespaces=self._namespaces, extensions=self._extensions,
            regexp=self._regexp, smart_strings=self._smart_strings)
        nodes = search(self._node)
        return self._get_guids(nodes)

    def get_child_guids(self, node_name: str, namespace: str = 'ocx') -> Callable:
        search = etree.XPath(
            path=OcxPathBuilder.select_nodes_with_attributes_name(
                attribute_name='GUIDRef'),
            namespaces=self._namespaces, extensions=self._extensions,
            regexp=self._regexp, smart_strings=self._smart_strings)
        nodes = search(self._node)
        return self._get_guids(nodes)
