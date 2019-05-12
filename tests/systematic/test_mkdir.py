from pathlib_fs import FsPath

import fs.path
from pathlib import Path

import pytest

def create_some_dir_in_tmpdir(general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  p.mkdir()
  yield
  with pytest.raises(Exception):
    p.mkdir()
  p.mkdir(exist_ok=True)

def test_check_with_pyfilesystem(general_fs_tmpdir):
  g = create_some_dir_in_tmpdir(general_fs_tmpdir)
  next(g)
  path = fs.path.join(general_fs_tmpdir.path, "some_dir")
  assert general_fs_tmpdir.fs.isdir(path)
  next(g, None)

def test_check_with_pathlib(general_osfs_tmpdir):
  g = create_some_dir_in_tmpdir(general_osfs_tmpdir)
  next(g)
  path = Path(general_osfs_tmpdir.os_path)/"some_dir"
  assert path.is_dir()
  next(g, None)

def test_check_self_consistency(general_fs_tmpdir):
  g = create_some_dir_in_tmpdir(general_fs_tmpdir)
  next(g)
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  assert p.is_dir()
  next(g, None)
