from pytest import mark

import os
import sys

from pathstring import Path


pytestmark = mark.skipif(sys.platform == "win32", reason="tests for posix only")

import grp


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


def test_group_should_get_group_name_from_group_database(fs):
    assert Path(fs, "file1.txt").group() == grp.getgrgid(os.getgid()).gr_name


@mark.skipif(sys.version_info < (3, 7), reason="added in python 3.7")
def test_is_mount_should_be_true_for_mount_points(fs):
    assert Path("/").is_mount()


@mark.skipif(sys.version_info < (3, 7), reason="added in python 3.7")
def test_is_mount_should_be_false_for_regular_directories(fs):
    assert not Path(fs).is_mount()
