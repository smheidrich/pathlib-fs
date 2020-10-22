from fs.enums import ResourceType
import fs.osfs
import fs.permissions
import pathlib
import os


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

  @classmethod
  def cwd(cls, disallow_str=False):
    # cf. comment on home() above
    cwd_parts = pathlib.Path.cwd().parts
    root = cwd_parts[0]
    rest = cwd_parts[1:] if len(cwd_parts) > 1 else ""
    return cls(fs.osfs.OSFS(root), *rest, disallow_str=disallow_str)

  # methods that emulate pathlib via PyFilesystem

  def open(self, *args, **kwargs):
    return self.fs.open(self.relative_fs_path, *args, **kwargs)

  def touch(self):
    self.fs.touch(self.relative_fs_path)

  def mkdir(self, mode=0o777, parents=False, exist_ok=False):
    permissions = fs.permissions.Permissions(mode=mode)
    if parents and self.parts and not self.parent.is_dir():
      # it's fine to only progress up to where the PyFilesystem part of the
      # path starts, as the former is guaranteed to exist (at least for OSFS),
      # so we never have to create it
      self.parent.mkdir(mode=mode, parents=parents, exist_ok=True)
    self.fs.makedir(self.relative_fs_path, permissions=permissions,
      recreate=exist_ok)

  def rename(self, target):
    if isinstance(target, FsPath):
      if target.fs != self.fs:
        raise ValueError("rename is only supported for {} objects based on "\
          "the same PyFilesystem object".format(self.__class__.__name__))
      target = target.relative_fs_path
    else:
      raise NotImplementedError("")
      # what should happen here:
      # - relative paths are interpreted as relative to cwd by pathlib => only
      #   makes sense for isinstance(fs, OsFs)
      # - absolute paths need some method of being interpreted with respect to
      #   FS (probably also only makes sense for OsFs, doesn't it?)
    self.fs.move(self.relative_fs_path, target, overwrite=False)

  def rmdir(self):
    self.fs.removedir(self.relative_fs_path)

  def unlink(self):
    self.fs.remove(self.relative_fs_path)

  def chmod(self, mode):
    raise NotImplementedError("PyFilesystem has no chmod() equivalent that I "
      "know of, so {}.chmod won't work either".format(self.__class__.__name__))
    # this is how it *would* work, if it was implemented properly in
    # PyFilesystem...
    permissions = fs.permissions.Permissions(mode=mode)
    print(oct(permissions.mode))
    info_dict = {
      "access": {
        "permissions": mode
      }
    }
    self.fs.setinfo(self.relative_fs_path, info_dict)

  def symlink_to(self, other):
    raise NotImplementedError("how does one create symlinks in PyFilesystem? "\
      "let me know at https://github.com/smheidrich/pathlib-fs/issues/new")

  def exists(self):
    return self.fs.exists(self.relative_fs_path)

  def is_block_device(self):
    return self.fs.gettype(self.relative_fs_path) == \
      ResourceType.block_special_file

  def is_char_device(self):
    return self.fs.gettype(self.relative_fs_path) == ResourceType.character

  def is_dir(self):
    return self.fs.isdir(self.relative_fs_path)

  def is_file(self):
    return self.fs.isfile(self.relative_fs_path)

  def is_fifo(self):
    return self.fs.gettype(self.relative_fs_path) == ResourceType.fifo

  def is_socket(self):
    return self.fs.gettype(self.relative_fs_path) == ResourceType.socket

  def is_symlink(self):
    # TODO report this to PyFilesystem... islink should just return False if
    # the path doesn't exist, because isfile and isdir do the same; but right
    # now it raises an exception, so we have to do this roundabout thing
    return self.exists() and self.fs.islink(self.relative_fs_path)

  def iterdir(self):
    return self.fs.listdir(self.relative_fs_path)

  def __eq__(self, other):
    if not isinstance(other, FsPath):
        return NotImplemented
    return super().__eq__(other) and self.fs == other.fs

  def owner(self):
    info = self.fs.getinfo(self.relative_fs_path, namespaces=["access"])
    if info.has_namespace("access"):
      return info.user
    else:
      return None

  def group(self):
    info = self.fs.getinfo(self.relative_fs_path, namespaces=["access"])
    if info.has_namespace("access"):
      return info.group
    else:
      return None

  def stat(self):
    fields = ["mode", "ino", "dev", "nlink", "uid", "gid", "size", "atime",
      "mtime", "ctime"]
    info = self.fs.getinfo(self.relative_fs_path, namespaces=["stat"])
    if info.has_namespace("stat"):
      return os.stat_result([info.raw["stat"]["st_"+x] for x in fields])
    else:
      return None

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

  def as_uri(self):
    return self.fs.geturl(self.relative_fs_path)

  # stuff that can just wrap pathlib methods directly
  # TODO I probably have to overwrite just one internal method to make all of
  # these work without having to write them here...

  def __truediv__(self, x):
    p = super().__truediv__(x)
    return self.__class__(self.fs, *(p.parts), disallow_str=self.disallow_str)

  def with_name(self, name):
    p = super().with_name(name)
    return self.__class__(self.fs, *(p.parts), disallow_str=self.disallow_str)

  def with_suffix(self, suffix):
    p = super().with_suffix(suffix)
    return self.__class__(self.fs, *(p.parts), disallow_str=self.disallow_str)

  @property
  def parent(self):
    p = super().parent
    return self.__class__(self.fs, *(p.parts), disallow_str=self.disallow_str)

  @property
  def parents(self):
    if len(self.parts) == 1:
      return [ self.parent ]
    else:
      return [ self.parent ] + self.parent.parents

  def relative_to(self, other):
    if isinstance(other, FsPath):
      if other.fs != self.fs:
        raise ValueError("relative_to is only supported for {} objects based "\
          "on the same PyFilesystem object".format(self.__class__.__name__))
    else:
      raise NotImplementedError("no idea what should happen here...")
    # TODO I'm returning a PurePath here because relative paths IMO don't make
    # sense for FsPaths... but yeah no idea really
    return pathlib.PurePath(*(super().relative_to(other).parts))

  def expanduser(self):
    # do nothing, as this can't be implemented in a general fashion
    return self

  # debug stuff

  # TODO this is actually not a good idea, because most of the object-creating
  # methods call this internally, and it's fine as long as e.g. the fs attribute
  # is handled separately:

  # def _from_parsed_parts(self, *args, **kwargs):
    # raise NotImplementedError("if this method ever gets called, some other "\
      # "method isn't working properly yet")
