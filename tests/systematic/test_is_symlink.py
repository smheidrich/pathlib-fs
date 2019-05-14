from pathlib_fs import FsPath

import fs.path
from pathlib import Path

import pytest

def script(perform, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
  p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
  p3 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_link")
  assert not p3.is_symlink()
  perform()
  assert not p.is_symlink()
  assert not p2.is_symlink()
  assert p3.exists()
  assert p3.is_symlink()

@pytest.mark.xfail(strict=True)
def test_perform_with_pyfilesystem(general_fs_tmpdir):
  def perform():
    path = fs.path.join(general_fs_tmpdir.path, "some_file")
    path2 = fs.path.join(general_fs_tmpdir.path, "some_dir")
    path3 = fs.path.join(general_fs_tmpdir.path, "some_link")
    general_fs_tmpdir.fs.touch(path)
    general_fs_tmpdir.fs.makedir(path2)
    # TODO I have no idea how to do this is PyFilesystem so this fails...
    general_fs_tmpdir.fs.symlink_to(path3, path)
  script(perform, general_fs_tmpdir)

def test_perform_with_pathlib(general_osfs_tmpdir):
  def perform():
    path = Path(general_osfs_tmpdir.os_path)/"some_file"
    path2 = Path(general_osfs_tmpdir.os_path)/"some_dir"
    path3 = Path(general_osfs_tmpdir.os_path)/"some_link"
    path.touch()
    path2.mkdir()
    path3.symlink_to(path)
  script(perform, general_osfs_tmpdir)

@pytest.mark.xfail(strict=True)
def test_perform_self_consistency(general_fs_tmpdir):
  def perform():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_dir")
    p3 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_link")
    p.touch()
    p2.mkdir()
    # TODO not implemented yet...
    p3.symlink_to(p)
  script(perform, general_fs_tmpdir)
