from typing import Any, Generator, IO, List, Optional, Sequence, Tuple, Type, Union

import os

__version__ = ...  # type: str

class Path(str):
    parts: Tuple[str, ...]
    drive: str
    root: str
    anchor: str
    name: str
    suffix: str
    suffixes: List[str]
    stem: str
    parent: Path
    parents: Sequence[Path]
    def __new__(cls: Type[Path], *args: Union[str, Path]) -> Path: ...
    def __truediv__(self, key: Union[str, Path]) -> Path: ...
    def __rtruediv__(self, key: Union[str, Path]) -> Path: ...
    def as_posix(self) -> str: ...
    def as_uri(self) -> str: ...
    def is_absolute(self) -> bool: ...
    def is_reserved(self) -> bool: ...
    def match(self, path_pattern: str) -> bool: ...
    def relative_to(self, other: Path, strict: bool = ...) -> Path: ...
    def with_name(self, name: str) -> Path: ...
    def with_suffix(self, suffix: str) -> Path: ...
    def joinpath(self: Path, *other: Union[str, Path]) -> Path: ...
    @classmethod
    def cwd(cls) -> Path: ...
    def stat(self) -> os.stat_result: ...
    def chmod(self, mode: int) -> None: ...
    def exists(self) -> bool: ...
    def glob(self, pattern: str) -> Generator[Path, None, None]: ...
    def group(self) -> str: ...
    def is_dir(self) -> bool: ...
    def is_file(self) -> bool: ...
    def is_mount(self) -> bool: ...
    def is_symlink(self) -> bool: ...
    def is_socket(self) -> bool: ...
    def is_fifo(self) -> bool: ...
    def is_block_device(self) -> bool: ...
    def is_char_device(self) -> bool: ...
    def iterdir(self) -> Generator[Path, None, None]: ...
    def lchmod(self, mode: int) -> None: ...
    def lstat(self) -> os.stat_result: ...
    def mkdir(self, mode: int = ..., parents: bool = ..., exist_ok: bool = ...) -> None: ...
    def open(
        self,
        mode: str = ...,
        buffering: int = ...,
        encoding: Optional[str] = ...,
        errors: Optional[str] = ...,
        newline: Optional[str] = ...,
    ) -> IO[Any]: ...
    def owner(self) -> str: ...
    def rename(self, target: Path) -> None: ...
    def resolve(self, strict: bool = ...) -> Path: ...
    def rglob(self, pattern: str) -> Generator[Path, None, None]: ...
    def rmdir(self) -> None: ...
    def rmtree(self, ignore_errors: bool = ..., onerror: bool = ...) -> None: ...
    def symlink_to(self, target: Path, target_is_directory: bool = ...) -> None: ...
    def touch(self, mode: int = ..., exist_ok: bool = ...) -> None: ...
    def unlink(self) -> None: ...
    @classmethod
    def home(cls) -> Path: ...
    def absolute(self) -> Path: ...
    def expanduser(self) -> Path: ...
    def read_bytes(self) -> bytes: ...
    def read_text(self, encoding: Optional[str] = ..., errors: Optional[str] = ...) -> str: ...
    def write_bytes(self, data: bytes) -> int: ...
    def samefile(self, other_path: Path) -> bool: ...
    def write_text(
        self, data: str, encoding: Optional[str] = ..., errors: Optional[str] = ...
    ) -> int: ...
