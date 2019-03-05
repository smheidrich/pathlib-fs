from pathlib_fs import FsPath

import fs.osfs
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

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
  pass

def test_basic_pathlib_emulation():
  """
  Tests that basic functionality emulating pathlib works
  """
  root = fs.osfs.OSFS("/tmp")
  p = FsPath(root, "hello/world")
  p2 = p / "etc"
  assert p2.as_str() == "/tmp/hello/world/etc"
  assert p2.relative_fs_path == "hello/world/etc"
  p3 = p.parent
  assert p3.as_str() == "/tmp/hello"

def test_open():
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    with (tmpdir_path/"some_file").open("w") as f:
      f.write("hello")
    root = fs.osfs.OSFS(tmpdir)
    p = FsPath(root, "some_file")
    with p.open() as f:
      assert f.read() == "hello"
    # also test another way of addressing the file just to be sure:
    root = fs.osfs.OSFS(tmpdir_path.parts[0])
    p = FsPath(root, Path(*tmpdir_path.parts[1:])/"some_file")
    with p.open() as f:
      assert f.read() == "hello"

def test_mkdir():
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    root = fs.osfs.OSFS(tmpdir)
    p = FsPath(root, "some_dir")
    p.mkdir()
    assert (tmpdir_path/"some_dir").is_dir()
    with pytest.raises(Exception):
      p.mkdir()
    p.mkdir(exist_ok=True)
    (p/"subdir1"/"subdir2").mkdir(parents=True)
    assert (tmpdir_path/"some_dir"/"subdir1"/"subdir2").is_dir()
