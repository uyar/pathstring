from typing import Any, Generator, IO, Optional, Tuple, Union

__version__ = ...  # type: str

import os

class Path(str):
    parts = ...  # type: Tuple[str, ...]
    name = ...  # type: str
    suffix = ...  # type: str
    stem = ...  # type: str
    parent = ...  # type: Path
    def __new__(cls, *args) -> Path: ...
    @classmethod
    def cwd(cls) -> Path: ...
    @classmethod
    def home(cls) -> Path: ...
    def absolute(self) -> Path: ...
    def resolve(self) -> Path: ...
    def with_name(self, name: str) -> Path: ...
    def with_suffix(self, suffix: str) -> Path: ...
    def glob(self, pattern: str) -> Generator[Path]: ...
    def is_absolute(self) -> bool: ...
    def stat(self) -> os.stat_result: ...
    def exists(self) -> bool: ...
    def is_dir(self) -> bool: ...
    def is_file(self) -> bool: ...
    def is_symlink(self) -> bool: ...
    def mkdir(self, mode: int = ..., parents: bool = ..., exist_ok: bool = ...) -> None: ...
    def rmdir(self) -> None: ...
    def symlink_to(self, target: Path, target_is_directory: bool = ...) -> None: ...
    def open(
        self,
        mode: str = ...,
        buffering: int = ...,
        encoding: Optional[str] = ...,
        errors: Optional[str] = ...,
        newline: Optional[str] = ...,
    ) -> IO[Any]: ...
    def touch(self, mode: int = ..., exist_ok: bool = ...) -> None: ...
    def unlink(self) -> None: ...
    def read_bytes(self) -> bytes: ...
    def read_text(self, encoding: Optional[str] = ..., errors: Optional[str] = ...) -> str: ...
    def write_bytes(self, data: bytes) -> int: ...
    def write_text(
        self, data: str, encoding: Optional[str] = ..., errors: Optional[str] = ...
    ) -> int: ...
    def samefile(self, other_path: Path) -> bool: ...
    def relative_to(self, other: Path, strict: Bool = ...) -> Path: ...
    def rmtree(self, ignore_errors: bool = ..., onerror: bool = ...) -> None: ...
