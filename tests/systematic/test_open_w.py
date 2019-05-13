from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def script(yield_f, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  with p.open("w") as f:
    f.write("hello")
  with yield_f() as f:
    assert f.read() == "hello"

def test_check_with_pyfilesystem(general_fs_tmpdir):
  def yield_f():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    return general_fs_tmpdir.fs.open(path)
  script(yield_f, general_fs_tmpdir)

def test_check_with_pathlib(general_osfs_tmpdir):
  def yield_f():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    return path.open()
  script(yield_f, general_osfs_tmpdir)

def test_check_self_consistency(general_fs_tmpdir):
  def yield_f():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    return p.open()
  script(yield_f, general_fs_tmpdir)
