from pytest import mark, raises

import sys
from os.path import pardir, sep
from pkg_resources import get_distribution

from pathstring import __version__, Path


def test_version():
    assert get_distribution("pathstring").version == __version__


def test_single_segment_should_be_same_as_input():
    assert Path("setup.py") == "setup.py"


def test_multiple_segments_should_be_concatenated_on_posix():
    assert Path("foo", "some/path", "bar") == "foo/some/path/bar".replace("/", sep)


def test_multiple_path_segments_should_be_concatenated():
    assert Path(Path("foo"), Path("bar")) == "foo/bar".replace("/", sep)


def test_no_segment_should_be_current_directory():
    assert Path() == "."


@mark.skipif(sys.platform == "win32", reason="posix behaviour")
def test_multiple_absolute_paths_should_anchor_to_last_on_posix():
    assert Path("/etc", "/usr", "lib64") == "/usr/lib64"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_multiple_absolute_paths_should_anchor_to_last_on_windows():
    assert Path("c:\\Windows", "d:bar") == "d:bar"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_changing_local_root_should_not_discard_drive():
    assert Path("c:\\Windows", "\\Program Files") == "c:\\Program Files"


def test_spurious_slashes_should_be_collapsed():
    assert Path("foo//bar") == "foo/bar".replace("/", sep)


def test_single_dots_should_be_collapsed():
    assert Path("foo/./bar") == "foo/bar".replace("/", sep)


def test_double_dots_should_be_collapsed():
    assert Path("foo/../bar") == "foo/../bar".replace("/", sep)


def test_relative_to_target_starting_with_parent_folder_should_fail_when_strict():
    with raises(ValueError):
        Path("d1", "d2", "f").relative_to(Path("d1", "d3"))


def test_relative_to_target_in_same_folder_should_be_target_name():
    assert Path("d1", "f").relative_to(Path("d1")).parts == ("f",)


def test_relative_to_target_in_child_folder_should_start_with_child():
    assert Path("d1", "d2", "f").relative_to(Path("d1")).parts == ("d2", "f")


def test_relative_to_target_in_grandchild_folder_should_start_with_two_children():
    assert Path("d1", "d2", "d3", "f").relative_to(Path("d1")).parts == ("d2", "d3", "f")


def test_relative_to_target_in_parent_folder_should_start_with_parent():
    assert Path("d1", "f").relative_to(Path("d1", "d2"), strict=False).parts == (pardir, "f")


def test_relative_to_target_in_grandparent_folder_should_start_with_two_parents():
    assert Path("d1", "f").relative_to(Path("d1", "d2", "d3"), strict=False).parts == (
        pardir,
        pardir,
        "f",
    )


def test_relative_to_target_in_diagonal_folder_should_go_up_and_down_when_not_stict():
    assert Path("d1", "d2", "f").relative_to(Path("d1", "d3"), strict=False).parts == (
        pardir,
        "d2",
        "f",
    )
