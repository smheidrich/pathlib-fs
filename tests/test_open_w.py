from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def write_some_file_in_tmpdir(general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  with p.open("w") as f:
    f.write("hello")

def check_file_contents(f):
  assert f.read() == "hello"

def test_open_write_file_check_with_pyfilesystem(general_fs_tmpdir):
  write_some_file_in_tmpdir(general_fs_tmpdir)
  path = fs.path.join(general_fs_tmpdir.path, "some_file")
  with general_fs_tmpdir.fs.open(path) as f:
    check_file_contents(f)

def test_open_write_file_osfs_check_with_pathlib(general_osfs_tmpdir):
  write_some_file_in_tmpdir(general_osfs_tmpdir)
  path = Path(general_osfs_tmpdir.os_path)/"some_file"
  with path.open() as f:
    check_file_contents(f)

def test_open_write_file_check_self_consistency(general_fs_tmpdir):
  write_some_file_in_tmpdir(general_fs_tmpdir)
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  with p.open() as f:
    check_file_contents(f)
