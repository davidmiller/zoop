"""
Enums.

Nicer Python mappings to the ZooKeeper constants
"""
import zookeeper

class Event(object):
    "Enum For ZooKeeper Event types"
    NotWatching = zookeeper.NOTWATCHING_EVENT
    Session = zookeeper.SESSION_EVENT
    Created = zookeeper.CREATED_EVENT
    Deleted = zookeeper.DELETED_EVENT
    Changed = zookeeper.CHANGED_EVENT
    Child   = zookeeper.CHILD_EVENT

