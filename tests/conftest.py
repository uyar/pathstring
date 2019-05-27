from pytest import fixture

import os
import sys
from shutil import rmtree
from tempfile import gettempdir


@fixture
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

    yield root

    rmtree(root)
