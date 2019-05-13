from pathlib_fs import FsPath

import fs.path
from pathlib import Path

def script(perform1, perform2, perform3, general_fs_tmpdir):
  p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "")
  assert len(set(p.iterdir())) == 0
  perform1()
  assert set(p.iterdir()) == set(["sub"])
  perform2()
  assert set(p.iterdir()) == set(["sub", "some_file"])
  perform3()
  assert set(p.iterdir()) == set(["sub", "some_file"])

def test_perform_with_pyfilesystem(general_fs_tmpdir):
  def perform1():
    path = fs.path.join(general_fs_tmpdir.path, "sub")
    general_fs_tmpdir.fs.makedir(path)
  def perform2():
    path2 = fs.path.join(general_fs_tmpdir.path, "some_file")
    general_fs_tmpdir.fs.touch(path2)
  def perform3():
    path3 = fs.path.join(general_fs_tmpdir.path, "sub/some_file")
    general_fs_tmpdir.fs.touch(path3)
  script(perform1, perform2, perform3, general_fs_tmpdir)

def test_perform_with_pathlib(general_osfs_tmpdir):
  def perform1():
    path = Path(general_osfs_tmpdir.os_path)/"sub"
    path.mkdir()
  def perform2():
    path2 = Path(general_osfs_tmpdir.os_path)/"some_file"
    path2.touch()
  def perform3():
    path3 = Path(general_osfs_tmpdir.os_path)/"sub/some_file"
    path3.touch()
  script(perform1, perform2, perform3, general_osfs_tmpdir)

def test_perform_self_consistency(general_fs_tmpdir):
  def perform1():
    p = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "sub")
    p.mkdir()
  def perform2():
    p2 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "some_file")
    p2.touch()
  def perform3():
    p3 = FsPath(general_fs_tmpdir.fs, general_fs_tmpdir.path, "sub/some_file")
    p3.touch()
  script(perform1, perform2, perform3, general_fs_tmpdir)
