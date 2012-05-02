"""
Make us a package  please!
"""
from zoop._version import __version__
from zoop import exceptions
from zoop.client import ZooKeeper
from zoop.enums import Event
from zoop.logutils import divert_zoolog
from zoop.queue import Queue

__all__ = [
    'exceptions',
    'ZooKeeper',
    '__version__',
    'divert_zoolog',
    'Event',
    'Queue'
    ]
