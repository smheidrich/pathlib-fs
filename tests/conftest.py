from collections import namedtuple
from contextlib import contextmanager
import fs.memoryfs
import fs.osfs
import fs.path
import fs.tempfs
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


DumbFsPath = namedtuple("DumbFsPath", ["fs", "path"])
DumbOsFsPath = namedtuple("DumbOsFsPath", ["fs", "path", "os_path"])

@contextmanager
def direct_osfs_tmpdir():
  with TemporaryDirectory() as tmpdir:
    _fs = fs.osfs.OSFS(tmpdir)
    yield DumbOsFsPath(_fs, "", tmpdir)

@contextmanager
def root_based_osfs_tmpdir():
  with TemporaryDirectory() as tmpdir:
    path = Path(tmpdir)
    _fs = fs.osfs.OSFS(path.parts[0])
    yield DumbOsFsPath(_fs, str(Path(*path.parts[1:])), tmpdir)

@pytest.fixture(params=[direct_osfs_tmpdir, root_based_osfs_tmpdir])
def general_osfs_tmpdir(request):
  with request.param() as dumb_fs_path:
    yield dumb_fs_path

@contextmanager
def tmpfs_tmpdir():
  _fs = fs.memoryfs.MemoryFS()
  try:
    yield DumbFsPath(_fs, "")
  finally:
    _fs.close()

@contextmanager
def memoryfs_tmpdir():
  _fs = fs.tempfs.TempFS()
  yield DumbFsPath(_fs, "")


@pytest.fixture(params=[
  direct_osfs_tmpdir, root_based_osfs_tmpdir, tmpfs_tmpdir, memoryfs_tmpdir
])
def general_fs_tmpdir(request):
  with request.param() as dumb_fs_path:
    yield dumb_fs_path

