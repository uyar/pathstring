from pytest import mark, raises

import os.path
import sys
from pkg_resources import get_distribution

from pathstring import __version__, Path


def test_version():
    assert get_distribution("pathstring").version == __version__


def test_single_segment_should_be_same_as_input():
    assert Path("setup.py") == "setup.py"


def test_multiple_segments_should_be_concatenated_on_posix():
    assert Path("foo", "some/path", "bar") == "foo/some/path/bar".replace("/", os.path.sep)


def test_multiple_path_segments_should_be_concatenated():
    assert Path(Path("foo"), Path("bar")) == "foo/bar".replace("/", os.path.sep)


def test_no_segment_should_be_current_directory():
    assert Path() == "."


def test_spurious_slashes_should_be_collapsed():
    assert Path("foo//bar") == "foo/bar".replace("/", os.path.sep)


def test_single_dots_should_be_collapsed():
    assert Path("foo/./bar") == "foo/bar".replace("/", os.path.sep)


def test_double_dots_should_not_be_collapsed():
    assert Path("foo/../bar") == "foo/../bar".replace("/", os.path.sep)


# TODO: case-sensitivity, equality, truediv (?)


def test_parts_should_be_a_sequence_of_components():
    assert Path("/usr/bin/python3").parts == (os.path.sep, "usr", "bin", "python3")


def test_root_should_be_path_separator():
    assert Path("/etc").root == os.path.sep


def test_root_for_relative_path_should_be_empty():
    assert Path("etc").root == ""


# TODO: ".anchor" tests


def test_parents_should_be_a_sequence_of_paths():
    assert list(Path("/foo/bar/setup.py").parents) == [
        p.replace("/", os.path.sep) for p in ["/foo/bar", "/foo", "/"]
    ]


def test_parent_should_be_parent_directory():
    assert Path("/a/b/c/d").parent == "/a/b/c".replace("/", os.path.sep)


def test_parent_should_not_go_past_anchor():
    assert Path("/").parent == os.path.sep


def test_parent_should_not_go_past_empty_path():
    assert Path(".").parent == "."


def test_parent_should_be_lexical_operation():
    assert Path("foo/..").parent == "foo"


def test_name_should_be_base_name():
    assert Path("my/library/setup.py").name == "setup.py"


def test_suffix_should_be_extension_of_final_component():
    assert Path("my/library/setup.py").suffix == ".py"


def test_suffix_should_be_last_extension_of_final_component():
    assert Path("my/library.tar.gz").suffix == ".gz"


def test_suffix_none_should_be_empty_string():
    assert Path("my/library").suffix == ""


def test_suffixes_should_be_a_sequence_of_extensions_of_final_component():
    assert Path("my/library.tar.gz").suffixes == [".tar", ".gz"]


def test_suffixes_should_be_a_sequence_even_if_single():
    assert Path("my/library.tar").suffixes == [".tar"]


def test_suffixes_none_should_be_empty_sequence():
    assert Path("my/library").suffixes == []


def test_stem_should_be_base_name_without_suffix():
    assert Path("my/library.tar").stem == "library"


def test_stem_should_be_base_name_without_only_last_suffix():
    assert Path("my/library.tar.gz").stem == "library.tar"


def test_stem_should_be_base_name_if_no_suffix():
    assert Path("my/library").stem == "library"


def test_joinpath_should_extend_current_path():
    assert Path("/etc").joinpath("passwd") == "/etc/passwd"


def test_joinpath_should_extend_current_path_with_path():
    assert Path("/etc").joinpath(Path("passwd")) == "/etc/passwd"


def test_joinpath_should_extend_current_path_with_multiple_segments():
    assert Path("/etc").joinpath("init.d", "apache2") == "/etc/init.d/apache2"


def test_match_relative_pattern_should_match_relative_path():
    assert Path("a/b.py").match("*.py")


def test_match_relative_pattern_should_match_absolute_path_from_the_right():
    assert Path("/a/b/c.py").match("b/*.py")


def test_match_relative_pattern_should_not_match_absolute_path_from_the_left():
    assert not Path("/a/b/c.py").match("a/*.py")


def test_match_absolute_pattern_should_match_absoluve_path():
    assert Path("/a.py").match("/*.py")


def test_match_absolute_pattern_should_not_match_absoluve_path_partially():
    assert not Path("a/b.py").match("/*.py")


# TODO: case-sensitive match (?)


def test_relative_to_target_in_child_directory_should_start_with_child():
    assert Path("/etc/passwd").relative_to(Path("/")) == "etc/passwd".replace("/", os.path.sep)


def test_relative_to_target_in_same_directory_should_be_target_name():
    assert Path("/etc/passwd").relative_to(Path("/etc")) == "passwd"


def test_relative_to_requiring_parent_directory_should_fail_when_strict():
    with raises(ValueError):
        Path("/etc/passwd").relative_to(Path("/usr"))
