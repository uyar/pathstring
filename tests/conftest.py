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

    with open(os.path.join(root, "file1.txt"), "wb") as f:
        f.write(b"1234")

    with open(os.path.join(root, "file2.txt"), "w", encoding="utf-8") as f:
        f.write("yağış")

    with open(os.path.join(root, "mod1.py"), "wb") as f:
        f.write(b"")

    os.makedirs(os.path.join(root, "sub"))
    with open(os.path.join(root, "sub", "mod2.py"), "wb") as f:
        f.write(b"")

    yield root

    rmtree(root, ignore_errors=True)
