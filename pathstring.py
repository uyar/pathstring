# Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>

"""Helpers for file system path operations."""

import os
import types
from inspect import signature
from itertools import dropwhile, zip_longest
from pathlib import Path as P
from shutil import rmtree


__version__ = "0.1.0"


def _make_path_type(name):
    def new_path(cls, *args):
        return str.__new__(cls, str(P(*args)))

    def get_property(prop, *, as_path=False):
        def f(self):
            result = getattr(P(self), prop)
            return result if not as_path else Path(result)

        return f

    def get_method(meth, *, class_method=False, as_path=False):
        m = getattr(P, meth)

        def f(*args, **kwargs):
            if not class_method:
                self, *rest = args
                args = (P(self),) + tuple(rest)
            result = m(*args, **kwargs)
            if isinstance(result, types.GeneratorType):
                return (Path(p) for p in result)
            return result if not as_path else Path(result)

        f.__signature__ = signature(m)
        f.__name__ = m.__name__
        f.__doc__ = m.__doc__

        return f

    def relative_to(self, other, strict=True):
        """Get the relative path of this path starting from another path."""
        if strict:
            return P(self).relative_to(other)
        parts = zip_longest(other.absolute().parts, self.absolute().parts)
        path_diff = dropwhile(lambda ps: ps[0] == ps[1], parts)
        up_parts, down_parts = zip(*path_diff)
        up_path = Path(*[os.path.pardir for p in up_parts if p is not None])
        down_path = Path(*[p for p in down_parts if p is not None])
        return Path(up_path, down_path)

    attrs = {}
    attrs["__new__"] = new_path
    for attr in ["parts", "name", "suffix", "stem"]:
        attrs[attr] = property(get_property(attr), doc=getattr(P, attr).__doc__)
    for attr in ["parent"]:
        attrs[attr] = property(get_property(attr, as_path=True), doc=getattr(P, attr).__doc__)
    for method in ["cwd", "home"]:
        attrs[method] = get_method(method, class_method=True, as_path=True)
    for method in ["absolute", "resolve", "with_name", "with_suffix", "glob"]:
        attrs[method] = get_method(method, as_path=True)
    for method in [
        "is_absolute",
        "stat",
        "exists",
        "is_dir",
        "is_file",
        "is_symlink",
        "mkdir",
        "rmdir",
        "symlink_to",
        "open",
        "touch",
        "unlink",
        "read_bytes",
        "read_text",
        "write_bytes",
        "write_text",
        "samefile",
    ]:
        attrs[method] = get_method(method)
    attrs["relative_to"] = relative_to
    attrs["rmtree"] = rmtree

    return type(name, (str,), attrs)


Path = _make_path_type("Path")
Path.__doc__ = "A path in the file system."
