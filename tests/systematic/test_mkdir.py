from pathlib_fs import FsPath

import fs.path
from pathlib import Path

import pytest

def segmented_script(f):
  class Wrapped:
    def __init__(self, *args, **kwargs):
      self.args, self.kwargs = args, kwargs
    def __enter__(self):
      self.gen = f(*self.args, **self.kwargs)
      next(self.gen)
      return self
    def __next__(self):
      return next(self.gen)
    def __exit__(self, exc_type, exc_value, traceback):
      try:
        next(self.gen)
      except StopIteration:
        return
      raise RuntimeError("generator not empty upon leaving context - most "\
          "likely there is something wrong with your segmented script")
  return Wrapped

@pytest.fixture()
def runner():
  @segmented_script
  def create_some_dir_in_tmpdir(general_fs_tmpdir):
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
    p.mkdir()
    yield
    with pytest.raises(Exception):
      p.mkdir()
    p.mkdir(exist_ok=True)
    yield
    print("hiya")
  yield create_some_dir_in_tmpdir

def test_check_with_pyfilesystem(general_fs_tmpdir, runner):
  with runner(general_fs_tmpdir) as r:
    path = fs.path.join(general_fs_tmpdir.path, "some_dir")
    assert general_fs_tmpdir.fs.isdir(path)
    next(r)

def test_check_with_pathlib(general_osfs_tmpdir, runner):
  with runner(general_osfs_tmpdir) as r:
    path = Path(general_osfs_tmpdir.os_path)/"some_dir"
    assert path.is_dir()
    next(r)

def test_check_self_consistency(general_fs_tmpdir, runner):
  with runner(general_fs_tmpdir) as r:
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
    assert p.is_dir()
    next(r)
