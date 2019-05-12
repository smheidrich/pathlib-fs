from pathlib_fs import FsPath

import fs.path
from pathlib import Path

import pytest

def script(check1, check2, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  p.mkdir()
  check1()
  with pytest.raises(Exception):
    p.mkdir()
  p.mkdir(exist_ok=True)
  (p/"subdir1"/"subdir2").mkdir(parents=True)
  check2()

def test_check_with_pyfilesystem(general_fs_tmpdir):
  def check1():
    path = fs.path.join(general_fs_tmpdir.path, "some_dir")
    assert general_fs_tmpdir.fs.isdir(path)
  def check2():
    path = fs.path.join(general_fs_tmpdir.path, "some_dir/subdir1/subdir2")
    assert general_fs_tmpdir.fs.isdir(path)
  script(check1, check2, general_fs_tmpdir)

def test_check_with_pathlib(general_osfs_tmpdir):
  def check1():
    path = Path(general_osfs_tmpdir.os_path)/"some_dir"
    assert path.is_dir()
  def check2():
    path = Path(general_osfs_tmpdir.os_path)/"some_dir/subdir1/subdir2"
    assert path.is_dir()
  script(check1, check2, general_osfs_tmpdir)

def test_check_self_consistency(general_fs_tmpdir):
  def check1():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
    assert p.is_dir()
  def check2():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path,
      "some_dir/subdir1/subdir2")
    assert p.is_dir()
  script(check1, check2, general_fs_tmpdir)
