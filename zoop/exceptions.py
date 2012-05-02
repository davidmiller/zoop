"""
Exceptions for the zoop library
"""
class Error(Exception):
    "Base Error from which all zoop exceptions must inherit"

class NoEventError(Error):
    "We wanted an event, but didn't get one."

class LostConnectionError(Error):
    "Lost connection to the ZooKeeper instance"

class NodeExistsError(Error):
    "The Node Exists!"

class NoNodeError(Error):
    "This Node does not exist"

class Empty(Error):
    "The item in question is empty."
