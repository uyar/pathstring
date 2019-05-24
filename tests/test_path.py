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


def test_parts_should_be_a_sequence_of_components():
    assert Path("/usr/bin/python3").parts == (sep, "usr", "bin", "python3")


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_anchor_should_be_a_separate_part_on_windows():
    assert Path("c:\\Program Files\\PSF").parts == ("c:\\", "Program Files", "PSF")


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_drive_should_be_drive_letter_on_windows():
    assert Path("c:\\Program Files\\").drive == "c:"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_no_drive_should_be_empty_string_on_windows():
    assert Path("\\Program Files\\PSF").drive == ""


@mark.skipif(sys.platform == "win32", reason="posix behaviour")
def test_drive_should_always_be_empty_on_posix():
    assert Path("/etc").drive == ""


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_unc_shares_should_be_considered_as_drives_on_windows():
    assert Path("\\\\host\\share\\foo.txt").drive == "\\\\host\\share"


@mark.skipif(sys.platform == "win32", reason="posix behaviour")
def test_root_should_be_separator_on_posix():
    assert Path("/etc").root == sep


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_root_should_be_separator_on_windows():
    assert Path("c:\\Program Files\\").root == sep


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_drive_should_not_be_part_of_root_on_windows():
    assert Path("c:Program Files\\").root == ""


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_unc_shares_should_always_have_a_root_on_windows():
    assert Path("\\\\host\\share\\").root == "\\"


# TODO: ".anchor" tests


def test_parents_should_be_a_sequence_of_paths():
    assert list(Path("/foo/bar/setup.py").parents) == [
        "/foo/bar".replace("/", sep),
        "/foo".replace("/", sep),
        "/".replace("/", sep),
    ]


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_parents_should_include_drive_on_windows():
    assert list(Path("c:\\foo\\bar\\setup.py").parents) == ["c:\\foo\\bar", "c:\\foo", "c:\\"]


def test_parent_should_be_parent_directory():
    assert Path("/a/b/c/d").parent == "/a/b/c".replace("/", sep)


def test_parent_should_not_go_past_anchor():
    assert Path("/").parent == sep


def test_parent_should_not_go_past_empty_path():
    assert Path(".").parent == "."


def test_parent_should_be_lexical_operation():
    assert Path("foo/..").parent == "foo"


def test_name_should_be_base_name():
    assert Path("my/library/setup.py").name == "setup.py"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_unc_base_names_should_be_considered_on_windows():
    assert Path("\\\\some\\share\\setup.py").name == "setup.py"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_unc_drive_names_should_be_considered_on_windows():
    assert Path("\\\\some\\share").name == ""


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


def test_stem_should_be_base_name_without_last_suffix():
    assert Path("my/library.tar.gz").stem == "library.tar"


def test_stem_should_be_base_name_if_no_suffix():
    assert Path("my/library").stem == "library"


@mark.skipif(sys.platform == "win32", reason="posix behaviour")
def test_as_posix_should_return_same_result_on_posix():
    assert Path("/etc/passwd").as_posix() == "/etc/passwd"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_as_posix_should_use_forward_slashes_on_windows():
    assert Path("c:\\windows").as_posix() == "c:/windows"


@mark.skipif(sys.platform == "win32", reason="posix behaviour")
def test_as_uri_should_return_uri():
    assert Path("/etc/passwd").as_uri() == "file:///etc/passwd"


@mark.skipif(sys.platform != "win32", reason="windows behaviour")
def test_as_uri_should_use_forward_slashes_on_windows():
    assert Path("c:\\windows").as_posix() == "file:///c:/Windows"


def test_relative_to_target_starting_with_parent_folder_should_fail_when_strict():
    with raises(ValueError):
        Path("d1/d2/f").relative_to(Path("d1/d3"))


def test_relative_to_target_in_same_folder_should_be_target_name():
    assert Path("d1/f").relative_to(Path("d1")) == "f"


def test_relative_to_target_in_child_folder_should_start_with_child():
    assert Path("d1/d2/f").relative_to(Path("d1")) == "d2/f".replace("/", sep)


def test_relative_to_target_in_grandchild_folder_should_start_with_two_children():
    assert Path("d1/d2/d3/f").relative_to(Path("d1")) == "d2/d3/f".replace("/", sep)


def test_relative_to_target_in_parent_folder_should_start_with_parent():
    assert Path("d1/f").relative_to(Path("d1/d2"), strict=False) == "../f".replace("/", sep)


def test_relative_to_target_in_grandparent_folder_should_start_with_two_parents():
    assert Path("d1/f").relative_to(Path("d1/d2/d3"), strict=False) == "../../f".replace(
        "/", sep
    )


def test_relative_to_target_in_diagonal_folder_should_go_up_and_down_when_not_stict():
    assert Path("d1/d2/f").relative_to(Path("d1/d3"), strict=False) == "../d2/f".replace(
        "/", sep
    )
