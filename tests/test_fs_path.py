from pathlib_fs import FsPath

import fs.osfs

import pytest

def test_representations():
  root = fs.osfs.OSFS("/tmp")
  p = FsPath(root, "hello/world")
  assert p.as_str() == "/tmp/hello/world"
  assert p.relative_fs_path == "hello/world"
  assert str(p) == "/tmp/hello/world"
  assert repr(p).startswith("FsPath(")
  assert "hello/world" in repr(p)
  with pytest.raises(ValueError):
    p_no_str = FsPath(root, "hello/world", disallow_str=True)
    str(p_no_str)
