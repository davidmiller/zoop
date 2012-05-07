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

    @classmethod
    def human(cls, item):
        """
        Given an integer representing an item in this Enum,
        fetch us the name of that property.


        Arguments:
        - `item`: int

        Return: str
        Exceptions: None
        """
        vals = cls.__dict__.values()
        thisone = [v for k, v in vals if v == item]
        return thisone[0]
