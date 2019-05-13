from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def script(check, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  p.touch()
  check()

def test_check_with_pyfilesystem(general_fs_tmpdir):
  def check():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    assert general_fs_tmpdir.fs.isfile(path)
  script(check, general_fs_tmpdir)

def test_check_with_pathlib(general_osfs_tmpdir):
  def check():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    assert path.is_file()
  script(check, general_osfs_tmpdir)

def test_check_self_consistency(general_fs_tmpdir):
  def check():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    assert p.is_file()
