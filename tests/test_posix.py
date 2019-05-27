from pytest import mark

import sys

from pathstring import Path


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
