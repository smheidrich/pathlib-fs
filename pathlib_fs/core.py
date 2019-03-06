import fs.osfs
import fs.permissions
import pathlib


class FsPath(pathlib.PosixPath):

  # constructors

  def __new__(cls, fs, *pathsegments, disallow_str=False):
    self = super().__new__(cls, *pathsegments)
    if self.is_absolute():
      raise ValueError("absolute paths don't make sense here...")
    self.fs = fs
    self.disallow_str = disallow_str
    return self

  @classmethod
  def home(cls, disallow_str=False):
    # we need an explicit reference here because super().home() would try to
    # instantiate using cls, which is our current class -> doesn't work
    home_parts = pathlib.Path.home().parts
    root = home_parts[0]
    rest = home_parts[1:] if len(home_parts) > 1 else ""
    return cls(fs.osfs.OSFS(root), *rest, disallow_str=disallow_str)

  # methods that emulate pathlib via PyFilesystem

  def open(self, *args, **kwargs):
    return self.fs.open(self.relative_fs_path, *args, **kwargs)

  def mkdir(self, mode=0o777, parents=False, exist_ok=False):
    permissions = fs.permissions.Permissions(mode=mode)
    if parents and self.parts and not self.parent.is_dir():
      # it's fine to only progress up to where the PyFilesystem part of the
      # path starts, as the former is guaranteed to exist (at least for OSFS),
      # so we never have to create it
      self.parent.mkdir(mode=mode, parents=parents, exist_ok=True)
    self.fs.makedir(self.relative_fs_path, permissions=permissions,
      recreate=exist_ok)

  def isdir(self):
    return self.fs.getinfo(self.relative_fs_path).is_dir

  # various "representations"

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

  # stuff that can just wrap pathlib methods directly
  # TODO I probably have to overwrite just one internal method to make all of
  # these work without having to write them here...

  def __truediv__(self, x):
    p = super().__truediv__(x)
    return self.__class__(self.fs, *(p.parts), disallow_str=self.disallow_str)

  @property
  def parent(self):
    p = super().parent
    return self.__class__(self.fs, *(p.parts), disallow_str=self.disallow_str)
