pathstring
==========

pathstring is a very small module that provides only one class
(``pathstring.Path``) which is a string with support for path operations.
Technically, it subclasses ``str`` and delegates path related operations to
``pathlib.Path``.

Differences from pathlib paths are:

- Paths are strings, no need to cast them to strings.

- No distinction between "pure" and "concrete" paths.

- No explicit distinction between Posix and Windows paths, but paths are
  always "native" to their platform.

- Adds a ``Path.rmtree()`` method which invokes ``shutil.rmtree()``
  on the path. Actually, since paths are strings, ``shutil.rmtree(path)``
  will also work.

- Supports the ``walk_up`` parameter to the ``Path.relative_to()`` method
  which, when set to ``True``, will also navigate "up" in the hierarchy.

- No support for case-insensitive comparisons on Windows.

- No ``Path.replace()`` method since it would cause confusion with
  ``str.replace()``.

Features are tested extensively against `pathlib documentation`_ to guarantee
compatibility.

License
-------

Copyright (C) 2019-2024 H. Turgut Uyar <uyar@tekir.org>

pathstring is released under the BSD license. Read the included
``LICENSE.txt`` file for details.

.. _pathlib documentation: https://docs.python.org/3/library/pathlib.html
