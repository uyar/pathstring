from pytest import mark, raises

import os
import shutil
import sys

from pathstring import Path

if sys.platform != "win32":
    import grp
    import pwd


pytestmark = mark.skipif(sys.platform == "win32", reason="tests for posix only")


def test_multiple_absolute_paths_should_anchor_to_last():
    assert Path("/etc", "/usr", "lib64") == "/usr/lib64"


def test_drive_should_be_empty():
    assert Path("/etc").drive == ""


def test_as_posix_should_return_same_result():
    assert Path("/etc/passwd").as_posix() == "/etc/passwd"


def test_as_uri_should_return_file_uri():
    assert Path("/etc/passwd").as_uri() == "file:///etc/passwd"


def test_is_absolute_when_starts_with_root():
    assert Path("/a/b").is_absolute()


def test_is_not_absolute_when_no_root():
    assert not Path("a/b").is_absolute()


def test_is_reserved_should_be_false():
    assert not Path("nul").is_reserved()


def test_stat_should_contain_permissions(fs):
    assert Path(fs, "file1.txt").stat().st_mode == 33188


def test_chmod_should_change_permissions(fs):
    Path(fs, "file1.txt").chmod(0o444)
    assert Path(fs, "file1.txt").stat().st_mode == 33060
    Path(fs, "file1.txt").chmod(0o644)
    assert Path(fs, "file1.txt").stat().st_mode == 33188


def test_group_should_get_group_name_from_group_database(fs):
    assert Path(fs, "file1.txt").group() == grp.getgrgid(os.getgid()).gr_name


@mark.skipif(sys.version_info < (3, 7), reason="added in python 3.7")
def test_is_mount_should_be_true_for_mount_points(fs):
    assert Path("/").is_mount()


@mark.skipif(sys.version_info < (3, 7), reason="added in python 3.7")
def test_is_mount_should_be_false_for_regular_directories(fs):
    assert not Path(fs).is_mount()


# TODO: ".is_symlink()", ".is_socket()", ".is_fifo()" tests
# TODO: ".is_block_device()", ".is_char_device()" tests
# TODO: ".lchmod()", ".lstat()" tests


def test_mkdir_should_create_directory_with_default_permissions(fs):
    path = os.path.join(fs, "tmp")
    Path(fs, "tmp").mkdir()
    assert os.stat(path).st_mode == 16877
    os.rmdir(path)


def test_mkdir_should_create_directory_with_given_permissions(fs):
    path = os.path.join(fs, "tmp")
    Path(fs, "tmp").mkdir(mode=0o555)
    assert os.stat(path).st_mode == 16749
    os.rmdir(path)


def test_owner_should_get_user_name_from_operating_system(fs):
    assert Path(fs, "file1.txt").owner() == pwd.getpwuid(os.getuid()).pw_name


def test_rename_should_overwrite_existing_target(fs):
    src = os.path.join(fs, "copy1.txt")
    shutil.copyfile(os.path.join(fs, "file1.txt"), src)
    dst = os.path.join(fs, "copy2.txt")
    shutil.copyfile(os.path.join(fs, "file2.txt"), dst)
    Path(src).rename(Path(dst))
    with open(dst, "rb") as f:
        content = f.read()
    assert content == b"file1"
    os.unlink(dst)


def test_symlink_to_directory_should_create_symbolic_link(fs):
    sublink1 = os.path.join(fs, "sublink1")
    Path(sublink1).symlink_to(Path(fs, "sub1"))
    assert os.path.exists(os.path.join(sublink1, "mod2.py"))


# TODO: Add test for touch with mode


def test_unlink_should_not_remove_directory_even_if_empty(fs):
    sub2 = os.path.join(fs, "sub2")
    os.mkdir(sub2)
    with raises(IsADirectoryError):
        Path(sub2).unlink()
