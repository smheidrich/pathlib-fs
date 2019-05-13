[![travis](https://travis-ci.org/smheidrich/pathlib-fs.svg?branch=master)](https://travis-ci.org/smheidrich/pathlib-fs)
[![codecov](https://codecov.io/gh/smheidrich/pathlib-fs/branch/master/graph/badge.svg)](https://codecov.io/gh/smheidrich/pathlib-fs)

# [WIP] pathlib-fs

[``pathlib.Path``](https://docs.python.org/3/library/pathlib.html) interface
for [PyFilesystem](https://www.pyfilesystem.org/).

## What?

See also: https://github.com/PyFilesystem/pyfilesystem2/issues/238

PyFilesystem provides a unified interface for dealing with various kinds of
(generalized) "filesystems", e.g. the regular local filesystem, a virtual
in-memory filesystem, filesystems on remote machines, ...

Meanwhile, a lot of libraries already use ``pathlib.Path`` for dealing with
operations on the local filesystem.

Now if only there was a wrapper around PyFilesystem paths exposing a
``pathlib.Path`` interface, all of these libraries would automatically gain
support for the various filesystems supported by PyFilesystem, so long as they
consequently deal with paths only via ``pathlib.Path`` methods (and don't
convert the path to a string before opening, etc.).

That's what this project aims to implement.

## API

To start with, the API will be as close as possible to ``pathlib.Path``'s, the
only exception being the constructor, which reads:

```python
FsPath(fs, *path_segments)
```

- ``fs``: PyFilesystem FS object
- ``*path_segments``: same meaning as ``pathlib.Path``

Note that ``path_segments`` *must* be relative, as paths in PyFilesystem are
always relative to the FS object.

### Extensions

Eventually, there will also be extensions beyond the ``pathlib.Path`` interface
for "missing" (in my opinion, anyway) functionality such as copying.

Whether these will be added in the form of subclass methods etc. is still TBD.

## Implementation status

Just started, hence totally WIP.

### Individual methods and properties

There is a lot to do...

I'm just going through ``pathlib.Path``'s methods and re-implementing them in
the wrapper one by one (cf. list below).

If you need any of the ones that aren't implemented yet, feel free to open a
ticket and I'll prioritize those.

#### Regular methods

- Done
    - ``exists``: done
    - ``home``: done
    - ``is_dir``: done
    - ``is_file``: done
    - ``iterdir``: done
    - ``mkdir``: done
    - ``name``: done (implicitly)
    - ``open``: done
    - ``parent``: done
    - ``parents``: done
    - ``parts``: done (implicitly)
    - ``rename``: done (with caveats)
    - ``stem``: done (implicitly)
    - ``suffix``: done (implicitly)
    - ``suffixes``: done (implicitly)
    - ``touch``: done
    - ``unlink``: done
    - ``with_name``: done
    - ``with_suffix``: done
- To do
    - ``anchor``: ?
    - ``as_posix``: ?
    - ``as_uri``: ?
    - ``cwd``: ?
    - ``expanduser``: ?
    - ``glob``: ?
    - ``group``: ?
    - ``is_block_device``: ?
    - ``is_char_device``: ?
    - ``is_fifo``: ?
    - ``is_mount``: ?
    - ``is_reserved``: ?
    - ``is_socket``: ?
    - ``is_symlink``: ?
    - ``joinpath``: ?
    - ``lchmod``: ?
    - ``lstat``: ?
    - ``match``: ?
    - ``owner``: ?
    - ``read_bytes``: ?
    - ``read_text``: ?
    - ``relative_to``: ?
    - ``replace``: ?
    - ``rglob``: ?
    - ``rmdir``: ?
    - ``samefile``: ?
    - ``stat``: ?
    - ``symlink_to``: ?
    - ``write_bytes``: ?
    - ``write_text``: ?
- To do, not clear what should happen
    - ``absolute``: ?
    - ``chmod``: blocked by unavailability in PyFilesystem itself...
    - ``drive``: ?
    - ``is_absolute``: ?
    - ``root``: ?
    - ``resolve``: ?

#### Special methods

- Done
    - ``__new__``: done
    - ``__repr__``: done
    - ~~``__init__``~~: already covered by ``__new__``
    - ``__str__``: done (extension: can be forbidden)
    - ``__truediv__``: done
- To do
    - ``__bytes__``: ?
    - ``__class__``: ?
    - ``__delattr__``: ?
    - ``__dir__``: ?
    - ``__doc__``: ?
    - ``__enter__``: ?
    - ``__eq__``: ?
    - ``__exit__``: ?
    - ``__format__``: ?
    - ``__fspath__``: ?
    - ``__ge__``: ?
    - ``__getattribute__``: ?
    - ``__gt__``: ?
    - ``__hash__``: ?
    - ``__init_subclass__``: ?
    - ``__le__``: ?
    - ``__lt__``: ?
    - ``__module__``: ?
    - ``__ne__``: ?
    - ``__reduce__``: ?
    - ``__reduce_ex__``: ?
    - ``__setattr__``: ?
    - ``__sizeof__``: ?
    - ``__slots__``: ?
    - ``__subclasshook__``: ?
- To do, not clear what should happen
    - ~~``__rtruediv__``~~ probably doesn't make sense?

#### Internal methods

I don't think I should implement any of those... but for completeness's sake:

- ``_accessor``: ?
- ``_cached_cparts``: ?
- ``_closed``: ?
- ``_cparts``: ?
- ``_drv``: ?
- ``_format_parsed_parts``: ?
- ``_from_parsed_parts``: ?
- ``_from_parts``: ?
- ``_hash``: ?
- ``_init``: ?
- ``_make_child``: ?
- ``_make_child_relpath``: ?
- ``_opener``: ?
- ``_parse_args``: ?
- ``_parts``: ?
- ``_pparts``: ?
- ``_raise_closed``: ?
- ``_raw_open``: ?
- ``_root``: ?
- ``_str``: ?


## Related projects

- [plumbum](https://plumbum.readthedocs.io/): has ``LocalPath`` and
  ``RemotePath`` classes, which are almost (but not quite yet) compatible with
  ``pathlib.Path``. If you just need a local/remote abstraction, these can be
  used for much the same purposes as this project here.
- [fspatch](https://github.com/PyFilesystem/fspatch): from what I understand,
  the aim of this is to be able to patch Python standard library modules to use
  PyFilesystem internally. If this is ever finished, it would probably make
  this wrapper pointless (?)
