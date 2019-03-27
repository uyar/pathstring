pathstring is a very small module that provides a string class
which supports path operations. Technically, it subclasses ``str``
and delegates path related operations to ``pathlib.Path``.

Differences from pathlib paths are:

- Paths are strings, no need to cast them to strings.

- It adds an ``rmtree`` operation which invokes ``shutil.rmtree``.
  Actually, since paths are also strings, in addition to ``path.rmtree()``,
  ``shutil.rmtree(path)`` will also work.

- It adds a ``strict`` parameter to the ``relative_to`` operation
  which, when set to ``False`` will also navigate up in the hierarchy.

License
-------

Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>

pathstring is released under the BSD license. Read the included
``LICENSE.txt`` file for details.
