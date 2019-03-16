# coding: utf-8
from setuptools import setup

setup(
  name="pathlib-fs",
  # version is handled dynamically by setuptools_scm
  use_scm_version = True,
  description="Pathlib interface for PyFilesystem objects",
  keywords="",
  url="",
  author="Shahriar Heidrich",
  author_email="smheidrich@weltenfunktion.de",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
  ],
  packages=["pathlib_fs"],
  setup_requires=[
    "pytest-runner",
    "setuptools_scm",
  ],
  install_requires=[
    "fs"
  ],
  tests_require=[
    "pytest",
    "testinfra",
  ],
)
