#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE
"""A python XPath implementation for OCX types"""

# System imports
from typing import Any, List

# Third party imports
from lxml import etree
from lxml.etree import XPathError

# Project imports


class OcxPathError(ValueError, XPathError):
    pass


class OcxPathBuilder:
    @staticmethod
    def select_all_named_nodes(nodename: str, namespace: str = "ocx") -> str:
        return f"//{namespace}:{nodename}"

    @staticmethod
    def select_current_node() -> str:
        return "."

    @staticmethod
    def select_parent_node() -> str:
        return "parent::*"

    @staticmethod
    def select_named_parent_node(parent: str, namespace: str = "ocx") -> str:
        return f"parent::{namespace}:{parent}"

    @staticmethod
    def select_named_nodes(node_name: str, namespace: str = "ocx") -> str:
        return f"//{namespace}:{node_name}"

    @staticmethod
    def select_any_nodes_with_global_attribute_name(
        attribute_name: str, namespace: str = "ocx"
    ) -> str:
        return f"//{namespace}:*[@{namespace}:{attribute_name}]"

    @staticmethod
    def select_any_nodes_with_attribute_value(
        attribute_name: str, attribute_value: str, namespace: str = "ocx"
    ) -> str:
        return f'//{namespace}:*[@{namespace}:{attribute_name}="{attribute_value}"]'

    @staticmethod
    def select_named_nodes_with_global_attribute_name(
        node_name: str, attribute_name: str, namespace: str = "ocx"
    ) -> str:
        return f"//{namespace}:{node_name}[@{namespace}:{attribute_name}]"

    @staticmethod
    def select_named_nodes_with_global_attribute_value(
        node_name: str,
        attribute_name: str,
        attribute_value: str,
        namespace: str = "ocx",
    ) -> str:
        return f'//{namespace}:{node_name}[@{namespace}:{attribute_name}="{attribute_value}"]'

    @staticmethod
    def select_any_nodes_with_local_attribute_name(
        attribute_name: str, namespace: str = "ocx"
    ) -> str:
        return f"//{namespace}:*[@{attribute_name}]"

    @staticmethod
    def select_any_nodes_with_local_value(
        attribute_name: str, attribute_value: str, namespace: str = "ocx"
    ) -> str:
        return f'//{namespace}:*[@{attribute_name}="{attribute_value}"]'

    @staticmethod
    def select_named_nodes_with_local_attribute_name(
        node_name: str, attribute_name: str, namespace: str = "ocx"
    ) -> str:
        return f"//{namespace}:{node_name}[@{attribute_name}]"

    @staticmethod
    def select_named_nodes_with_local_attribute_value(
        node_name: str,
        attribute_name: str,
        attribute_value: str,
        namespace: str = "ocx",
    ) -> str:
        return f'//{namespace}:{node_name}[@{attribute_name}="{attribute_value}"]'


class OcxPath:
    def __init__(
        self,
        document_root: etree.Element,
        namespaces: Any,
        extensions: Any = None,
        regexp: bool = True,
        smart_strings: bool = True,
    ):
        self._root = document_root
        self._namespaces = namespaces
        self._extensions = extensions
        self._regexp = regexp
        self._smart_strings = smart_strings

    def get_ocx_attribute_value_collection(
        self,
        element: etree.Element,
        attribute_name: str,
        namespace: str = "ocx",
    ) -> List[Any]:
        """

        Args:
            element: The lxml Element instance
            attribute_name: The attribute name to be retrieved
            namespace: Optional namespace prefix. Default = "ocx"

        Returns:
            A list of attributes.
        """
        search = etree.XPath(
            path=OcxPathBuilder.select_any_nodes_with_global_attribute_name(
                attribute_name=attribute_name, namespace=namespace
            ),
            namespaces=self._namespaces,
            regexp=self._regexp,
            smart_strings=self._smart_strings,
        )
        result = search(element)
        return [v.get(attribute_name) for v in result]

    def get_ocx_attribute_with_value(
        self,
        element: etree.Element,
        attribute_name: str,
        attribute_value: str,
        namespace: str = "ocx",
    ) -> List[Any]:
        """

        Args:
            element:
            attribute_name:
            attribute_value:
            namespace:

        Returns:

        """
        search = etree.XPath(
            path=OcxPathBuilder.select_any_nodes_with_attribute_value(
                attribute_name=attribute_name,
                attribute_value=attribute_value,
                namespace=namespace,
            ),
            namespaces=self._namespaces,
            regexp=self._regexp,
            smart_strings=self._smart_strings,
        )
        return search(element)

    def get_all_named_ocx_elements(
        self, name: str, namespace: str = "ocx"
    ) -> List[Any]:
        path = OcxPathBuilder.select_all_named_nodes(nodename=name, namespace=namespace)
        search = etree.XPath(
            path=path,
            namespaces=self._namespaces,
            regexp=self._regexp,
            smart_strings=self._smart_strings,
        )
        return search(self._root)

    def get_all_named_children(
        self, node: etree.Element, child_name: str, namespace: str = "ocx"
    ) -> List[Any]:
        search = etree.XPath(
            path=OcxPathBuilder.select_all_named_nodes(
                nodename=child_name, namespace=namespace
            ),
            namespaces=self._namespaces,
            regexp=self._regexp,
            smart_strings=self._smart_strings,
        )
        return search(node)
