import os.path

from pathstring import Path


def test_relative_to_target_in_parent_folder_should_start_with_parent():
    assert Path("d1/f").relative_to(Path("d1/d2"), strict=False) == "../f".replace(
        "/", os.path.sep
    )


def test_relative_to_target_in_grandparent_folder_should_start_with_two_parents():
    assert Path("d1/f").relative_to(Path("d1/d2/d3"), strict=False) == "../../f".replace(
        "/", os.path.sep
    )


def test_relative_to_target_in_diagonal_folder_should_go_up_and_down_when_not_stict():
    assert Path("d1/d2/f").relative_to(Path("d1/d3"), strict=False) == "../d2/f".replace(
        "/", os.path.sep
    )
