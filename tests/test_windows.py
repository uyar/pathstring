from pytest import mark, raises

import os
import shutil
import sys

from pathstring import Path


pytestmark = mark.skipif(sys.platform != "win32", reason="tests for windows only")


def test_multiple_absolute_paths_should_anchor_to_last():
    assert Path("c:\\Windows", "d:bar") == "d:bar"


def test_changing_local_root_should_not_discard_drive():
    assert Path("c:\\Windows", "\\Program Files") == "c:\\Program Files"


def test_drive_should_be_a_part_of_first_component():
    assert Path("c:\\Program Files\\PSF").parts == ("c:\\", "Program Files", "PSF")


def test_drive_should_be_drive_letter_with_colon():
    assert Path("c:\\Program Files\\").drive == "c:"


def test_empty_drive_should_be_empty_string():
    assert Path("\\Program Files\\PSF").drive == ""


def test_unc_shares_should_be_considered_drives():
    assert Path("\\\\host\\share\\foo.txt").drive == "\\\\host\\share"


def test_drive_should_not_be_part_of_root():
    assert Path("c:\\Program Files\\").root == "\\"


def test_drive_should_not_be_part_of_root_for_relative_path():
    assert Path("c:Program Files\\").root == ""


def test_unc_shares_should_always_have_a_root():
    assert Path("\\\\host\\share\\").root == "\\"


def test_parents_should_include_drive_letter():
    assert list(Path("c:\\foo\\bar\\setup.py").parents) == ["c:\\foo\\bar", "c:\\foo", "c:\\"]


def test_name_should_be_base_names_on_unc_shares():
    assert Path("\\\\some\\share\\setup.py").name == "setup.py"


def test_name_should_exclude_unc_share():
    assert Path("\\\\some\\share").name == ""


def test_as_posix_should_use_forward_slashes():
    assert Path("c:\\windows").as_posix() == "c:/windows"


def test_as_uri_should_use_forward_slashes():
    assert Path("c:\\Windows").as_uri() == "file:///c:/Windows"


def test_is_absolute_when_starts_with_drive_and_root():
    assert Path("c:\\a\\b").is_absolute()


def test_is_not_absolute_when_no_drive():
    assert not Path("\\a\\b").is_absolute()


def test_is_not_absolute_when_no_root():
    assert not Path("c:").is_absolute()


def test_is_absolute_when_starts_with_unc_share():
    assert Path("\\\\some\\share").is_absolute()


def test_is_reserved_should_be_true_for_reserved_paths():
    assert Path("nul").is_reserved()


def test_is_reserved_should_not_be_true_for_regular_paths():
    assert not Path("c:\\\\windows").is_reserved()


def test_joinpath_should_extend_drive_with_path():
    assert Path("c:").joinpath("\\Program Files") == "c:\\Program Files"


def test_relative_to_on_different_drive_should_fail_even_when_not_strict():
    with raises(ValueError):
        Path("c:\\windows").relative_to(Path("d:\\"), strict=False)


def test_rename_should_fail_for_existing_target(fs):
    src = os.path.join(fs, "copy1.txt")
    shutil.copyfile(os.path.join(fs, "file1.txt"), src)
    dst = os.path.join(fs, "copy2.txt")
    shutil.copyfile(os.path.join(fs, "file2.txt"), dst)
    with raises(FileExistsError):
        Path(src).rename(Path(dst))
    os.unlink(src)


def test_symlink_to_directory_should_create_symbolic_link(fs):
    sublink1 = os.path.join(fs, "sublink1")
    Path(sublink1).symlink_to(Path(fs, "sub1"), target_is_directory=True)
    assert os.path.exists(os.path.join(sublink1, "mod2.py"))


def test_unlink_should_not_remove_directory_even_if_empty(fs):
    sub2 = os.path.join(fs, "sub2")
    os.mkdir(sub2)
    with raises(PermissionError):
        Path(sub2).unlink()
