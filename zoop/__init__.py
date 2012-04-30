"""
Make us a package  please!
"""
from zoop import exceptions
from zoop.client import ZooKeeper
from zoop.logutils import divert_zoolog
from zoop.enums import Event
from zoop._version import __version__

__all__ = [
    'exceptions',
    'ZooKeeper',
    '__version__',
    'divert_zoolog',
    'Event'
    ]
