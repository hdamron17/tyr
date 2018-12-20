# Copyright Hunter Damron 2018

from setuptools import setup, find_packages
from tyr import VERSION

REPO_URL = "https://github.com/hdamron17/tyr"

setup(
  name="tyr",
  version=VERSION,
  packages=find_packages() + ["test"],
  entry_points = {
    "console_scripts": ["tyrc=tyr.tyrc:main"]
  },
  package_data = {
    "test": ["Makefile", "test.sh", "*.tyr", "output/*"],
    "tyr.llvm_code": ["*.ll"]
  },
  data_files = [
    ("", ["LICENSE.txt"])
  ],
  install_requires=[
    "docopt>=0.6.2"
  ],

  author = "Hunter Damron",
  author_email = "hdamron1594@yahoo.com",
  description = "A simple statically typed language compiler",
  license = "MIT",
  url = REPO_URL,
  project_urls = {
    "Source Code": REPO_URL
  }
)
