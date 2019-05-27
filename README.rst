pathstring is a very small module that provides a string class
which supports path operations. Technically, it subclasses ``str``
and delegates path related operations to ``pathlib.Path``.

Differences from pathlib paths are:

- Paths are strings, no need to cast them to strings. No distinction
  between "pure" and "concrete" paths.

- A ``path.rmtree()`` operation which invokes ``shutil.rmtree``.
  Actually, since paths are strings, ``shutil.rmtree(path)`` will also work.

- A ``strict`` parameter to the ``relative_to`` operation
  which, when set to ``False``, will also navigate up in the hierarchy.

- No support the slash operator for joining paths (for now).

- No support for case-insensitive equality checks on Windows (for now).

- No ``.replace`` method since it would cause confusion with ``str.replace``.

Features are tested extensively against `pathlib documentation`_ to guarantee
compatibility.

License
-------

Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>

pathstring is released under the BSD license. Read the included
``LICENSE.txt`` file for details.

.. _pathlib documentation: https://docs.python.org/3/library/pathlib.html
