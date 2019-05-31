from pytest import mark, raises

import os
import shutil
import sys
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


def test_slash_operator_should_create_child_paths():
    assert Path("/etc") / "init.d" / "apache2" == "/etc/init.d/apache2".replace(
        "/", os.path.sep
    )


def test_slash_operator_should_accept_paths_as_segments():
    assert Path("/usr") / Path("bin") == "/usr/bin".replace("/", os.path.sep)


def test_slash_operator_should_accept_paths_on_rhs():
    assert "/usr" / Path("bin") == "/usr/bin".replace("/", os.path.sep)


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
    assert Path(fs, "file1.txt").stat().st_size == 5


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
    assert set(Path(fs).glob("*/*.py")) == {os.path.join(fs, "sub1", "mod2.py")}


def test_glob_should_support_recursive_search_pattern(fs):
    assert set(Path(fs).glob("**/*.py")) == {
        os.path.join(fs, "mod1.py"),
        os.path.join(fs, "sub1", "mod2.py"),
    }


def test_is_dir_should_be_true_for_directories(fs):
    assert Path(fs, "sub1").is_dir()


def test_is_dir_should_be_false_for_files(fs):
    assert not Path(fs, "file1.txt").is_dir()


def test_is_file_should_be_true_for_files(fs):
    assert Path(fs, "file1.txt").is_file()


def test_is_file_should_be_false_for_directories(fs):
    assert not Path(fs, "sub1").is_file()


def test_is_symlink_should_be_true_for_symlinks(fs):
    assert Path(fs, "link1").is_symlink()


def test_is_symlink_should_be_false_for_files(fs):
    assert not Path(fs, "file1.txt").is_symlink()


def test_iterdir_should_return_sequence_of_directory_entries_non_recursively(fs):
    assert set(Path(fs).iterdir()) == {
        os.path.join(fs, de) for de in ["file1.txt", "file2.txt", "mod1.py", "link1", "sub1"]
    }


def test_mkdir_should_create_non_existing_directory(fs):
    path = os.path.join(fs, "tmp")
    assert not os.path.exists(path)
    Path(fs, "tmp").mkdir()
    assert os.path.exists(path)
    os.rmdir(path)


def test_mkdir_should_fail_nested_creation_if_parents_not_set(fs):
    with raises(FileNotFoundError):
        Path(fs, "tmp1", "tmp2").mkdir()


def test_mkdir_should_succeed_nested_creation_if_parents_set(fs):
    path1 = os.path.join(fs, "tmp1")
    path2 = os.path.join(path1, "tmp2")
    assert not os.path.exists(path1)
    Path(fs, "tmp1", "tmp2").mkdir(parents=True)
    assert os.path.exists(path2)
    os.rmdir(path2)
    os.rmdir(path1)


def test_mkdir_should_fail_for_existing_directory(fs):
    path = os.path.join(fs, "tmp")
    os.mkdir(path)
    with raises(FileExistsError):
        Path(fs, "tmp").mkdir()
    os.rmdir(path)


def test_mkdir_should_not_fail_for_existing_directory_if_exist_ok_is_set(fs):
    path = os.path.join(fs, "tmp")
    os.mkdir(path)
    Path(fs, "tmp").mkdir(exist_ok=True)
    assert os.path.exists(path)
    os.rmdir(path)


def test_open_should_open_file_compatible_with_builtin(fs):
    with Path(fs, "file1.txt").open("rb") as f:
        assert f.read() == b"file1"


def test_read_bytes_should_read_file_as_binary(fs):
    assert Path(fs, "file1.txt").read_bytes() == b"file1"


def test_read_text_should_read_text_as_str(fs):
    assert Path(fs, "file2.txt").read_text(encoding="utf-8") == "abcöüçğış"


def test_rename_should_rename_file_for_nonexisting_target(fs):
    src = os.path.join(fs, "copy1.txt")
    shutil.copyfile(os.path.join(fs, "file1.txt"), src)
    dst = os.path.join(fs, "renamed1.txt")
    Path(src).rename(Path(dst))
    with open(dst, "rb") as f:
        content = f.read()
    assert content == b"file1"
    os.unlink(dst)


def test_resolve_should_return_absolute_path(fs):
    assert Path().resolve() == os.getcwd()


@mark.skipif(sys.platform == "win32", reason="fails due to shortening of path")
def test_resolve_should_resolve_symbolic_link(fs):
    assert Path(fs, "link1").resolve() == os.path.join(fs, "file1.txt")


@mark.skipif(sys.version_info < (3, 6), reason="strict in python 3.5")
def test_resolve_should_eliminate_pardir(fs):
    assert Path("docs/../setup.py").resolve() == os.path.join(os.getcwd(), "setup.py")


@mark.skipif(sys.version_info < (3, 6), reason="added in python 3.6")
def test_resolve_should_fail_for_nonexisting_path_when_strict(fs):
    with raises(FileNotFoundError):
        Path("docs/../setup.py").resolve(strict=True)


@mark.skipif(sys.version_info >= (3, 6), reason="strict in python 3.5")
def test_resolve_should_fail_for_nonexisting_path(fs):
    with raises(FileNotFoundError):
        Path("docs/../setup.py").resolve()


def test_rglob_should_search_recursively(fs):
    assert set(Path(fs).rglob("*.py")) == {
        os.path.join(fs, "mod1.py"),
        os.path.join(fs, "sub1", "mod2.py"),
    }


def test_rmdir_should_remove_empty_directory(fs):
    sub2 = os.path.join(fs, "sub2")
    os.mkdir(sub2)
    Path(fs, "sub2").rmdir()
    assert not os.path.exists(sub2)


def test_rmdir_should_not_remove_nonempty_directory(fs):
    with raises(OSError):
        Path(fs, "sub1").rmdir()


def test_samefile_should_return_true_for_same_target(fs):
    assert Path(fs, "link1").samefile(Path(fs, "file1.txt"))


def test_samefile_should_return_false_for_different_targets(fs):
    assert not Path(fs, "link1").samefile(Path(fs, "file2.txt"))


def test_symlink_to_should_create_symbolic_link(fs):
    link2 = os.path.join(fs, "link2")
    Path(link2).symlink_to(Path(fs, "file2.txt"))
    with open(link2, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "abcöüçğış"
    os.unlink(link2)


def test_touch_should_create_empty_file(fs):
    path = os.path.join(fs, "tmp")
    assert not os.path.exists(path)
    Path(path).touch()
    assert os.path.exists(path)
    assert os.stat(path).st_size == 0
    os.unlink(path)


def test_touch_should_fail_for_existing_file_if_exist_ok_is_false(fs):
    path = os.path.join(fs, "file1.txt")
    with raises(FileExistsError):
        Path(path).touch(exist_ok=False)


def test_touch_should_change_mtime_of_existing_file(fs):
    path = os.path.join(fs, "file1.txt")
    mtime1 = os.stat(path).st_mtime
    Path(path).touch()
    mtime2 = os.stat(path).st_mtime
    assert mtime2 > mtime1


def test_unlink_should_remove_file(fs):
    src = os.path.join(fs, "copy1.txt")
    shutil.copyfile(os.path.join(fs, "file1.txt"), src)
    Path(src).unlink()
    assert not os.path.exists(src)


def test_unlink_should_remove_symlink(fs):
    file2 = os.path.join(fs, "file2.txt")
    link2 = os.path.join(fs, "link2")
    os.symlink(file2, link2)
    Path(link2).unlink()
    assert not os.path.exists(link2)
    assert os.path.exists(file2)


def test_unlink_should_fail_for_nonexisting_path(fs):
    with raises(FileNotFoundError):
        Path(fs, "file0.txt").unlink()


def test_write_bytes_should_write_file_as_binary(fs):
    path = os.path.join(fs, "file3.txt")
    Path(path).write_bytes(b"file3")
    with open(path, "rb") as f:
        content = f.read()
    assert content == b"file3"


def test_write_text_should_write_text_as_str(fs):
    path = os.path.join(fs, "file3.txt")
    Path(path).write_text("abcöüçğış", encoding="utf-8")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "abcöüçğış"


def test_rmtree_should_remove_tree_recursively(fs):
    tmp1 = os.path.join(fs, "tmp1")
    os.mkdir(tmp1)
    tmp2 = os.path.join(tmp1, "tmp2")
    os.mkdir(tmp2)
    tmp3 = os.path.join(tmp2, "tmp3.txt")
    shutil.copyfile(os.path.join(fs, "file1.txt"), tmp3)
    Path(tmp2).rmtree()
    assert not os.path.exists(tmp2)
    assert os.path.exists(tmp1)
    os.rmdir(tmp1)


def test_shutil_rmtree_should_take_path_as_parameter(fs):
    tmp1 = os.path.join(fs, "tmp1")
    os.mkdir(tmp1)
    tmp2 = os.path.join(tmp1, "tmp2")
    os.mkdir(tmp2)
    tmp3 = os.path.join(tmp2, "tmp3.txt")
    shutil.copyfile(os.path.join(fs, "file1.txt"), tmp3)
    shutil.rmtree(Path(tmp2))
    assert not os.path.exists(tmp2)
    assert os.path.exists(tmp1)
    os.rmdir(tmp1)


def test_rmtree_should_fail_for_nonexisting_directory(fs):
    with raises(FileNotFoundError):
        Path(fs, "tmp1").rmtree()


def test_rmtree_should_not_fail_for_nonexisting_directory_if_ignoring_errors(fs):
    Path(fs, "tmp1").rmtree(ignore_errors=True)
