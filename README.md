# [WIP] pathlib-fs

[``pathlib.Path``](https://docs.python.org/3/library/pathlib.html) interface
for [PyFilesystem](https://www.pyfilesystem.org/).

## What?

PyFilesystem provides an unified interface for dealing with various kinds of
(generalized) "filesystems", e.g. the regular local filesystem, a virtual
in-memory filesystem, filesystems on remote machines, ...

Meanwhile, a lot of libraries already use ``pathlib.Path`` for dealing with
operations on the local filesystem.

Now if only there was a wrapper around PyFilesystem paths exposing a
``pathlib.Path`` interface, all of these libraries would automatically gain
support for the various filesystems supported by PyFilesystem, so long as they
consequently deal with paths only via ``pathlib.Path`` methods (and don't
convert the path to a string before opening, etc.).

That's what this project aims to provide.

## Implementation status

Just started, hence totally WIP.

### Individual methods and properties

There is a lot to do...

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
- ``__init__``: ?
- ``__init_subclass__``: ?
- ``__le__``: ?
- ``__lt__``: ?
- ``__module__``: ?
- ``__ne__``: ?
- ``__new__``: ?
- ``__reduce__``: ?
- ``__reduce_ex__``: ?
- ``__repr__``: ?
- ~~``__rtruediv__``~~ probably doesn't make sense?
- ``__setattr__``: ?
- ``__sizeof__``: ?
- ``__slots__``: ?
- **``__str__``**: done (extension: can be forbidden)
- ``__subclasshook__``: ?
- **``__truediv__``**: done
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
- ``absolute``: ?
- ``anchor``: ?
- ``as_posix``: ?
- ``as_uri``: ?
- ``chmod``: ?
- ``cwd``: ?
- ``drive``: ?
- ``exists``: ?
- ``expanduser``: ?
- ``glob``: ?
- ``group``: ?
- ``home``: ?
- ``is_absolute``: ?
- ``is_block_device``: ?
- ``is_char_device``: ?
- ``is_dir``: ?
- ``is_fifo``: ?
- ``is_file``: ?
- ``is_mount``: ?
- ``is_reserved``: ?
- ``is_socket``: ?
- ``is_symlink``: ?
- ``iterdir``: ?
- ``joinpath``: ?
- ``lchmod``: ?
- ``lstat``: ?
- ``match``: ?
- **``mkdir``**: done
- ``name``: ?
- **``open``**: done
- ``owner``: ?
- **``parent``**: done
- ``parents``: ?
- ``parts``: ?
- ``read_bytes``: ?
- ``read_text``: ?
- ``relative_to``: ?
- ``rename``: ?
- ``replace``: ?
- ``resolve``: ?
- ``rglob``: ?
- ``rmdir``: ?
- ``root``: ?
- ``samefile``: ?
- ``stat``: ?
- ``stem``: ?
- ``suffix``: ?
- ``suffixes``: ?
- ``symlink_to``: ?
- ``touch``: ?
- ``unlink``: ?
- ``with_name``: ?
- ``with_suffix``: ?
- ``write_bytes``: ?
- ``write_text``: ?


## Related projects

- [plumbum](https://plumbum.readthedocs.io/): has ``LocalPath`` and
  ``RemotePath`` classes , which are almost (but not quite yet) compatible with
  ``pathlib.Path``. If you just need a local/remote abstraction, these it can
  be used for much the same purposes as this project here.
