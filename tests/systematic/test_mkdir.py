from pathlib_fs import FsPath

import fs.path
from pathlib import Path

import pytest

def script(check, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  p.mkdir()
  check()
  with pytest.raises(Exception):
    p.mkdir()
  p.mkdir(exist_ok=True)

def test_check_with_pyfilesystem(general_fs_tmpdir):
  def check():
    path = fs.path.join(general_fs_tmpdir.path, "some_dir")
    assert general_fs_tmpdir.fs.isdir(path)
  script(check, general_fs_tmpdir)

def test_check_with_pathlib(general_osfs_tmpdir):
  def check():
    path = Path(general_osfs_tmpdir.os_path)/"some_dir"
    assert path.is_dir()
  script(check, general_osfs_tmpdir)

def test_check_self_consistency(general_fs_tmpdir):
  def check():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
    assert p.is_dir()
  script(check, general_fs_tmpdir)
