from pathlib_fs import FsPath

import fs.memoryfs
import fs.osfs
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

def root_based_fspath(dir_path, relative_fs_path):
  path = dir_path/relative_fs_path
  root_fs = fs.osfs.OSFS(path.parts[0])
  return FsPath(root_fs, Path(*path.parts[1:]))

def dir_based_fspath(dir_path, relative_file_path):
  dir_fs = fs.osfs.OSFS(dir_path)
  return FsPath(dir_fs, Path(relative_file_path))


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

@pytest.mark.parametrize("make_fs_path", [root_based_fspath, dir_based_fspath])
def test_touch_exists_is_file(make_fs_path):
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    tmpfile_path = tmpdir_path/"some_file"
    p = make_fs_path(tmpdir_path, "some_file")
    assert not p.exists()
    assert not p.is_file()
    p.touch()
    assert p.exists()
    assert p.is_file()
    assert tmpfile_path.exists()

def test_touch_exists_isfile_memoryfs():
  # this is to check that it doesn't just perform these operations via
  # pathlib.Path
  mem_fs = fs.memoryfs.MemoryFS()
  relative_path = Path("some_file")
  p = FsPath(mem_fs, relative_path)
  assert not relative_path.exists(), "sorry; clean up your working directory"
  assert not relative_path.is_file()
  assert not p.exists()
  assert not p.is_file()
  p.touch()
  assert p.exists()
  assert p.is_file()
  assert not relative_path.exists()
  assert not relative_path.is_file()

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

@pytest.mark.parametrize("make_fs_path", [root_based_fspath, dir_based_fspath])
def test_rename_unlink_using_fspath(make_fs_path):
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    tmpfile_path = tmpdir_path/"some_file"
    tmpfile2_path = tmpdir_path/"some_file2"
    p = make_fs_path(tmpdir_path, "some_file")
    p2 = p.parent/"some_file2"
    p.touch()
    p.rename(p2)
    assert not tmpfile_path.exists()
    assert tmpfile2_path.exists()
    tmpfile2_path.unlink()
    assert not tmpfile2_path.exists()

def test_is_dir():
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    root = fs.osfs.OSFS(tmpdir_path.parts[0])
    p = FsPath(root, Path(*tmpdir_path.parts[1:]))
    assert p.is_dir()

@pytest.mark.parametrize("make_fs_path", [root_based_fspath, dir_based_fspath])
def test_iterdir(make_fs_path):
  with TemporaryDirectory() as tmpdir:
    tmpdir_path = Path(tmpdir)
    p = make_fs_path(tmpdir_path, "")
    assert len(set(p.iterdir())) == 0
    sub_path = Path(tmpdir)/"sub"
    sub_path.mkdir()
    assert set(p.iterdir()) == set(["sub"])
    tmpfile_path = tmpdir_path/"some_file"
    tmpfile_path.touch()
    assert set(p.iterdir()) == set(["sub", "some_file"])
    tmpfile2_path = tmpdir_path/"some_file2"
    tmpfile2_path.touch()
    assert set(p.iterdir()) == set(["sub", "some_file", "some_file2"])
    subtmpfile_path = sub_path/"some_file"
    subtmpfile_path.touch()
    assert set(p.iterdir()) == set(["sub", "some_file", "some_file2"])

def test_home():
  h = FsPath.home()
  assert str(h) == str(Path.home())

