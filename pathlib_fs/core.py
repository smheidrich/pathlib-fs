import pathlib


class FsPath(pathlib.PosixPath):
  def __new__(cls, fs, *pathsegments, disallow_str=False):
    self = super().__new__(cls, *pathsegments)
    if self.is_absolute():
      raise ValueError("absolute paths don't make sense here...")
    self.fs = fs
    self.disallow_str = disallow_str
    return self

  def open(self, *args, **kwargs):
    return self.fs.open(self.as_str(), *args, **kwargs)

  @property
  def relative_fs_path(self) -> str:
    """
    The path relative to ``fs``, i.e. what PyFilesystem considers a path
    """
    return super().__str__()

  def as_pathlib_path(self):
    # this assumes that pathlib.Path -> Posix/Windows resolution will match how
    # PyFilesystem determines OS flavor... is this the case? not sure.
    # return pathlib.Path(self.fs.getospath(self.relative_fs_path))
    # TODO ^ this should work but getospath() returns bytes instead of str...
    # TODO --> report this as a bug!!
    return pathlib.Path(self.fs.getsyspath(self.relative_fs_path))

  def as_str(self):
    return str(self.as_pathlib_path())

  def __str__(self):
    if not self.disallow_str:
      return self.as_str()
    else:
      raise ValueError("str() not allowed for this {} instance".format(
        self.__class__))

  def __repr__(self):
    return "{}({}, {})".format(self.__class__.__name__, self.fs,
      repr(super().__str__()))

  def __truediv__(self, x):
    segments = list(self.parts) + [x]
    return self.__class__(self.fs, *segments, disallow_str=self.disallow_str)
