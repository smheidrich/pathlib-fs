from pathlib_fs import FsPath

import fs.memoryfs
import fs.path
from pathlib import Path

import pytest

def script(check1, check2, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file2")
  with pytest.raises(Exception):
    p.rename(p2)
  p.touch()
  p.rename(p2)
  check1()
  p2.unlink()
  check2()
  # test that this doesn't try to do anything across fs object boundaries
  other_mem_fs = fs.memoryfs.MemoryFS()
  relative_path = Path("some_file")
  p3 = FsPath(other_mem_fs, relative_path)
  p3.touch()
  with pytest.raises(ValueError):
    p3.rename(p2)
  p3.unlink()
  p2.touch()
  with pytest.raises(ValueError):
    p2.rename(p3)

def test_check_with_pyfilesystem(general_fs_tmpdir):
  def check1():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    path2 = fs.path.join(general_fs_tmpdir.path, "some_file2")
    assert not general_fs_tmpdir.fs.exists(path)
    assert general_fs_tmpdir.fs.exists(path2)
  def check2():
    path2 = fs.path.join(general_fs_tmpdir.path, "some_file2")
    assert not general_fs_tmpdir.fs.exists(path2)
  script(check1, check2, general_fs_tmpdir)

def test_check_with_pathlib(general_osfs_tmpdir):
  def check1():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    path2 = Path(general_osfs_tmpdir.os_path)/"some_file2"
    assert not path.exists()
    assert path2.exists()
  def check2():
    path2 = Path(general_osfs_tmpdir.os_path)/"some_file2"
    assert not path2.exists()
  script(check1, check2, general_osfs_tmpdir)

def test_check_self_consistency(general_fs_tmpdir):
  def check1():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file2")
    assert not p.exists()
    assert p2.exists()
  def check2():
    p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file2")
    assert not p2.exists()
  script(check1, check2, general_fs_tmpdir)
