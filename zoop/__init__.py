"""
Make us a package  please!
"""
from zoop.client import ZooKeeper
from zoop.logutils import divert_zoolog
from zoop._version import __version__

__all__ = [
    'ZooKeeper',
    '__version__',
    'divert_zoolog'
    ]
