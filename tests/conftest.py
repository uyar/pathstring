from pytest import fixture

import os
import sys
from shutil import rmtree
from tempfile import gettempdir


@fixture(scope="session")
def fs():
    """Root directory for test files hierarchy."""
    temp_dir = "/dev/shm"
    if (sys.platform != "linux") or (not os.path.exists(temp_dir)):
        temp_dir = gettempdir()
    root = os.path.join(temp_dir, "pathstring_tests")

    rmtree(root, ignore_errors=True)
    os.umask(0o022)
    os.makedirs(root)

    file1 = os.path.join(root, "file1.txt")
    with open(file1, "wb") as f:
        f.write(b"file1")

    file2 = os.path.join(root, "file2.txt")
    with open(file2, "w", encoding="utf-8") as f:
        f.write("abcöüçğış")

    mod1 = os.path.join(root, "mod1.py")
    with open(mod1, "wb") as f:
        f.write(b"mod1")

    sub1 = os.path.join(root, "sub1")
    os.makedirs(sub1)

    mod2 = os.path.join(sub1, "mod2.py")
    with open(mod2, "wb") as f:
        f.write(b"sub1.mod2")

    link1 = os.path.join(root, "link1")
    os.symlink(file1, link1)

    yield root

    rmtree(root, ignore_errors=True)
