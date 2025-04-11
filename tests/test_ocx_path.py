#  Copyright (c) 2024. #  OCX Consortium https://3docx.org. See the LICENSE


# Project imports

from ocx_common.x_path.x_path import OcxGuidRef, OcxPath

from .conftest import MODEL_FOLDER, TEST_MODEL


def test_find_vessel(load_model_1):
    root = load_model_1.get_root()
    ocx_path = OcxPath(root, namespaces=root.nsmap)
    node = ocx_path.get_all_named_ocx_elements(name="Vessel", namespace="ocx")
    assert len(node) == 1


def test_find_all_guids(load_model_1):
    root = load_model_1.get_root()
    guids = OcxGuidRef(root, namespaces=root.nsmap).get_all_guids()
    assert len(guids) == 25


def test_find_child_guids(load_model_1):
    root = load_model_1.get_root()

    guids = OcxGuidRef(root, namespaces=root.nsmap).get_child_guids("CoordinateSystem")
    assert len(guids) == 25


def test_get_all_named_nodes(load_model_1):
    root = load_model_1.get_root()
    nodes = OcxPath(root, namespaces=root.nsmap).get_all_named_ocx_elements(
        "CoordinateSystem"
    )
    assert len(nodes) == 1
