from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def script(yield_f, general_fs_tmpdir):
  with yield_f() as f:
    f.write("hello")
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  with p.open() as f:
    assert f.read() == "hello"
  with p.open("r") as f:
    assert f.read() == "hello"
  with p.open("rb") as f:
    assert f.read() == b"hello"

def test_perform_with_pyfilesystem(general_fs_tmpdir):
  def yield_f():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    return general_fs_tmpdir.fs.open(path, "w")
  script(yield_f, general_fs_tmpdir)

def test_perform_with_pathlib(general_osfs_tmpdir):
  def yield_f():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    return path.open("w")
  script(yield_f, general_osfs_tmpdir)

def test_perform_self_consistency(general_fs_tmpdir):
  def yield_f():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    return p.open("w")
  script(yield_f, general_fs_tmpdir)
