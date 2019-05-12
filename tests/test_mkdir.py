from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def create_some_dir_in_tmpdir(general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  p.mkdir()

def test_mkdir_check_with_pyfilesystem(general_fs_tmpdir):
  create_some_dir_in_tmpdir(general_fs_tmpdir)
  path = fs.path.join(general_fs_tmpdir.path, "some_dir")
  assert general_fs_tmpdir.fs.isdir(path)

def test_mkdir_check_with_pathlib(general_osfs_tmpdir):
  create_some_dir_in_tmpdir(general_osfs_tmpdir)
  path = Path(general_osfs_tmpdir.os_path)/"some_dir"
  assert path.is_dir()

def test_mkdir_check_self_consistency(general_fs_tmpdir):
  create_some_dir_in_tmpdir(general_fs_tmpdir)
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  assert p.is_dir()
