# flake8: noqa

from os.path import pardir
from pkg_resources import get_distribution

from pathstring import __version__, Path


def test_version():
    assert get_distribution("pathstring").version == __version__


def test_relative_from_target_in_same_folder_should_be_target_name():
    assert Path("d1", "f").relative_to(Path("d1")).parts == ("f",)


def test_relative_from_target_in_child_folder_should_start_with_child():
    assert Path("d1", "d2", "f").relative_to(Path("d1")).parts == ("d2", "f")


def test_relative_from_target_in_grandchild_folder_should_start_with_two_children():
    assert Path("d1", "d2", "d3", "f").relative_to(Path("d1")).parts == ("d2", "d3", "f")


def test_relative_from_target_in_parent_folder_should_start_with_parent():
    assert Path("d1", "f").relative_to(Path("d1", "d2")).parts == (pardir, "f")


def test_relative_from_target_in_grandparent_folder_should_start_with_two_parents():
    assert Path("d1", "f").relative_to(Path("d1", "d2", "d3")).parts == (pardir, pardir, "f")


def test_relative_from_target_in_diagonal_folder_should_go_up_and_down():
    assert Path("d1", "d2", "f").relative_to(Path("d1", "d3")).parts == (pardir, "d2", "f")
