import os.path

from pathstring import Path


def test_relative_to_requiring_parent_directory_should_start_with_pardir():
    assert Path("/etc/passwd").relative_to(
        Path("/etc/network"), strict=False
    ) == "../passwd".replace("/", os.path.sep).replace("..", os.path.pardir)


def test_relative_to_requiring_multiple_parent_directories_should_start_with_multiple_pardirs():
    assert Path("/etc/passwd").relative_to(
        Path("/usr/bin"), strict=False
    ) == "../../etc/passwd".replace("/", os.path.sep).replace("..", os.path.pardir)
