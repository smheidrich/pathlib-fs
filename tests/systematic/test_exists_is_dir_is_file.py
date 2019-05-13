from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def script(perform, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  assert not p.exists()
  assert not p.is_file()
  assert not p.is_dir()
  assert not p2.exists()
  assert not p2.is_file()
  assert not p2.is_dir()
  perform()
  assert p.exists()
  assert p.is_file()
  assert not p.is_dir()
  assert p2.exists()
  assert p2.is_dir()
  assert not p2.is_file()

def test_perform_with_pyfilesystem(general_fs_tmpdir):
  def perform():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    path2 = fs.path.join(general_fs_tmpdir.path, "some_dir")
    general_fs_tmpdir.fs.touch(path)
    general_fs_tmpdir.fs.makedir(path2)
  script(perform, general_fs_tmpdir)

def test_perform_with_pathlib(general_osfs_tmpdir):
  def perform():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    path2 = Path(general_osfs_tmpdir.os_path)/"some_dir"
    path.touch()
    path2.mkdir()
  script(perform, general_osfs_tmpdir)

def test_perform_self_consistency(general_fs_tmpdir):
  def perform():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
    p.touch()
    p2.mkdir()
  script(perform, general_fs_tmpdir)
