from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def write_some_file_in_tmpdir(general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  with p.open("w") as f:
    f.write("hello")
  f = yield
  assert f.read() == "hello"
  yield # dummy -> no StopIteration TODO

def test_check_with_pyfilesystem(general_fs_tmpdir):
  g = write_some_file_in_tmpdir(general_fs_tmpdir)
  next(g)
  path = fs.path.join(general_fs_tmpdir.path, "some_file")
  with general_fs_tmpdir.fs.open(path) as f:
    g.send(f)

def test_check_with_pathlib(general_osfs_tmpdir):
  g = write_some_file_in_tmpdir(general_osfs_tmpdir)
  next(g)
  path = Path(general_osfs_tmpdir.os_path)/"some_file"
  with path.open() as f:
    g.send(f)

def test_check_self_consistency(general_fs_tmpdir):
  g = write_some_file_in_tmpdir(general_fs_tmpdir)
  next(g)
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  with p.open() as f:
    g.send(f)
