from pathlib_fs import FsPath

import fs.memoryfs
import fs.osfs
import fs.path
from pathlib import Path, PurePath
from tempfile import TemporaryDirectory

import pytest

def root_based_fspath(dir_path, relative_fs_path):
  path = dir_path/relative_fs_path
  root_fs = fs.osfs.OSFS(path.parts[0])
  return FsPath(root_fs, Path(*path.parts[1:]))

def dir_based_fspath(dir_path, relative_file_path):
  dir_fs = fs.osfs.OSFS(dir_path)
  return FsPath(dir_fs, Path(relative_file_path))

def test_from_absolute_path():
  root = fs.osfs.OSFS("/tmp")
  with pytest.raises(ValueError):
    FsPath(root, "/hello/world")

def test_representations():
  """
  Test various representations of FsPath objects
  """
  root = fs.osfs.OSFS("/tmp")
  p = FsPath(root, "hello/world")
  assert p.as_str() == "/tmp/hello/world"
  assert p.as_pathlib_path() == Path("/tmp/hello/world")
  assert p.relative_fs_path == "hello/world"
  assert str(p) == "/tmp/hello/world"
  assert repr(p).startswith("FsPath(")
  assert "hello/world" in repr(p)
  assert p.parts == ("hello", "world") # TODO intended?
  with pytest.raises(ValueError):
    p_no_str = FsPath(root, "hello/world", disallow_str=True)
    str(p_no_str)

def test_pathlib_derived_functionality():
  """
  Tests that functionality derived from pathlib with no changes still works
  """
  root = fs.osfs.OSFS("/tmp")
  p = FsPath(root, "hello/world")
  assert p.name == "world"
  p2 = FsPath(root, "")
  assert p2.name == "" # TODO intended?
  p3 = p.with_name("universe")
  assert str(p3) == "/tmp/hello/universe"
  assert isinstance(p3, FsPath)
  p4 = p3.with_suffix(".xyz")
  assert str(p4) == "/tmp/hello/universe.xyz"
  assert isinstance(p4, FsPath)
  assert p4.suffix == ".xyz"
  assert p4.suffixes == [".xyz"]
  assert p4.stem == "universe"
  assert (p/"file.suf1.suf2").suffixes == [".suf1", ".suf2"]
  assert (p/"relative/test").relative_to(p) == PurePath("relative/test")
  with pytest.raises(ValueError):
    (p/"relative/test").relative_to(FsPath(fs.memoryfs.MemoryFS(), "tmp"))

def test_basic_pathlib_emulation():
  """
  Tests that basic functionality emulating pathlib works
  """
  root = fs.osfs.OSFS("/tmp")
  p = FsPath(root, "hello/world")
  p2 = p / "etc"
  assert p2.as_str() == "/tmp/hello/world/etc"
  assert p2.relative_fs_path == "hello/world/etc"
  assert p.fs == p2.fs
  p3 = p.parent
  assert p3.as_str() == "/tmp/hello"
  assert p == FsPath(root, "hello", "world")
  assert p != "hello/world" # just to make coverage happy...
  # print(list(p.parents))
  assert list(p.parents) == [ FsPath(root, "hello"), FsPath(root, "") ]

def test_read_write():
  root = fs.osfs.OSFS("/tmp")
  p = FsPath(root, "helloworld")
  p.write_text("foo")
  with open("/tmp/helloworld") as f:
    assert f.read() == "foo"
  assert p.read_text() == "foo"
  p.write_bytes(b"foo")
  with open("/tmp/helloworld", "rb") as f:
    assert f.read() == b"foo"
  assert p.read_bytes() == b"foo"


@pytest.mark.xfail(raises=NotImplementedError, strict=True)
@pytest.mark.parametrize("make_fs_path", [root_based_fspath, dir_based_fspath])
def test_chmod(make_fs_path):
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    tmpfile_path = tmpdir_path/"some_file"
    p = make_fs_path(tmpdir_path, "some_file")
    p.touch()
    p.chmod(0o715)
    assert (tmpfile_path.stat().st_mode & 0o777) == 0o715

@pytest.mark.xfail(strict=True)
@pytest.mark.parametrize("make_fs_path", [root_based_fspath, dir_based_fspath])
def test_rename_unlink_using_str(make_fs_path):
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    tmpfile_path = tmpdir_path/"some_file"
    tmpfile2_path = tmpdir_path/"some_file2"
    p = make_fs_path(tmpdir_path, "some_file")
    p.touch()
    p.rename(str(tmpdir_path/"some_file2"))
    assert not tmpfile_path.exists()
    assert tmpfile2_path.exists()
    tmpfile2_path.unlink()
    assert not tmpfile2_path.exists()
    p.touch()
    p.rename(str(tmpfile2_path))
    assert not tmpfile_path.exists()
    assert tmpfile2_path.exists()

def test_home():
  h = FsPath.home()
  assert str(h) == str(Path.home())

def test_cwd():
  h = FsPath.cwd()
  assert str(h) == str(Path.cwd())
