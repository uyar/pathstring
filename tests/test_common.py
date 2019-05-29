from pytest import raises

import os
import time

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


# TODO: truediv (?)


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
    assert Path("/etc").joinpath("passwd") == "/etc/passwd".replace("/", os.path.sep)


def test_joinpath_should_extend_current_path_with_path():
    assert Path("/etc").joinpath(Path("passwd")) == "/etc/passwd".replace("/", os.path.sep)


def test_joinpath_should_extend_current_path_with_multiple_segments():
    assert Path("/etc").joinpath("init.d", "apache2") == "/etc/init.d/apache2".replace(
        "/", os.path.sep
    )


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


def test_relative_to_target_in_child_directory_should_start_with_child():
    assert Path("/etc/passwd").relative_to(Path("/")) == "etc/passwd".replace("/", os.path.sep)


def test_relative_to_target_in_same_directory_should_be_target_name():
    assert Path("/etc/passwd").relative_to(Path("/etc")) == "passwd"


def test_relative_to_requiring_parent_directory_should_fail_when_strict():
    with raises(ValueError):
        Path("/etc/passwd").relative_to(Path("/usr"))


def test_relative_to_requiring_parent_directory_should_start_with_pardir():
    assert Path("/etc/passwd").relative_to(
        Path("/etc/network"), strict=False
    ) == "../passwd".replace("/", os.path.sep).replace("..", os.path.pardir)


def test_relative_to_requiring_multiple_parent_directories_should_start_with_multiple_pardirs():
    assert Path("/etc/passwd").relative_to(
        Path("/usr/bin"), strict=False
    ) == "../../etc/passwd".replace("/", os.path.sep).replace("..", os.path.pardir)


def test_with_name_should_return_path_with_changed_name():
    assert Path("/tmp/pathlib.tar.gz").with_name("setup.py") == "/tmp/setup.py".replace(
        "/", os.path.sep
    )


def test_with_name_should_fail_when_no_name_in_source():
    with raises(ValueError):
        Path("/").with_name("setup.py")


def test_with_suffix_should_return_path_with_changed_suffix():
    assert Path("/tmp/pathlib.tar.gz").with_suffix(".bz2") == "/tmp/pathlib.tar.bz2".replace(
        "/", os.path.sep
    )


def test_with_suffix_should_add_suffix_when_no_suffix_in_source():
    assert Path("README").with_suffix(".txt") == "README.txt"


def test_with_suffix_should_remove_suffix_when_no_suffix_in_destination():
    assert Path("README.txt").with_suffix("") == "README"


def test_cwd_should_return_same_as_getcwd():
    assert Path.cwd() == os.getcwd()


def test_home_should_return_home_directory_of_current_user():
    assert Path.home() == os.path.expanduser("~")


def test_stat_should_contain_file_size(fs):
    assert Path(fs, "file1.txt").stat().st_size == 4


def test_stat_should_contain_modification_time(fs):
    assert time.time() - Path(fs, "file1.txt").stat().st_mtime < 1


def test_exists_should_return_true_for_existing_file(fs):
    assert Path(fs, "file1.txt").exists()


def test_exists_should_return_false_for_nonexisting_file(fs):
    assert not Path(fs, "file0.txt").exists()


def test_expanduser_should_return_path_with_user_home_expanded():
    assert Path("~/films/Monty Python").expanduser() == os.path.join(
        os.path.expanduser("~"), "films", "Monty Python"
    )


def test_glob_should_return_sequence_of_matching_file_paths(fs):
    assert set(Path(fs).glob("*.txt")) == {
        os.path.join(fs, f) for f in ["file1.txt", "file2.txt"]
    }


def test_glob_should_return_sequence_even_when_only_one_result(fs):
    assert list(Path(fs).glob("*.py")) == [os.path.join(fs, "mod1.py")]


def test_glob_should_return_empty_sequence_even_no_result(fs):
    assert len(set(Path(fs).glob("*.mp4"))) == 0


def test_glob_should_be_able_to_search_in_subdirectories(fs):
    assert set(Path(fs).glob("*/*.py")) == {os.path.join(fs, "sub", "mod2.py")}


def test_glob_should_support_recursive_search_pattern(fs):
    assert set(Path(fs).glob("**/*.py")) == {
        os.path.join(fs, "mod1.py"),
        os.path.join(fs, "sub", "mod2.py"),
    }


def test_is_dir_should_be_true_for_directories(fs):
    assert Path(fs, "sub").is_dir()


def test_is_dir_should_be_false_for_files(fs):
    assert not Path(fs, "file1.txt").is_dir()


def test_is_file_should_be_true_for_files(fs):
    assert Path(fs, "file1.txt").is_file()


def test_is_file_should_be_false_for_directories(fs):
    assert not Path(fs, "sub").is_file()
