from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def script(perform, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  assert not p.exists()
  perform()
  assert p.exists()

def test_perform_with_pyfilesystem(general_fs_tmpdir):
  def perform():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    general_fs_tmpdir.fs.touch(path)
  script(perform, general_fs_tmpdir)

def test_perform_with_pathlib(general_osfs_tmpdir):
  def perform():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    path.touch()
  script(perform, general_osfs_tmpdir)

def test_perform_self_consistency(general_fs_tmpdir):
  def perform():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    p.touch()
  script(perform, general_fs_tmpdir)
