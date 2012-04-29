import re

from distutils.core import setup

VERSION_FILE = "zoop/_version.py"
verstrline = open(VERSION_FILE, "rt").read()
VSRE = r'^__version__ = [\'"]([^\'"]*)[\'"]'
mo = re.search(VSRE,  verstrline, re.M)
if mo:
    VERSION = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in {0}".format(VERSION_FILE))

setup(
    name = "zoop",
    version = VERSION,
    author = "David Miller",
    author_email = "david@deadpansincerity.com",
    url = "http://github.com/davidmiller/zoop",
    description = "Pythonic API for Zookeeper",
    long_description = open('README.rst').read() + "\n\n" +  open('HISTORY.rst').read(),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2.6",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
        ],
    packages = ['zoop'],
    )
