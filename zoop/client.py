"""
zoop.client
"""
from zoop._zookeeper import zookeeper

OPEN_ACL_UNSAFE = dict(perms=zookeeper.PERM_ALL, scheme = 'world', id='anyone')


class ZooKeeper(object):
    """
    The ZooKeeper client

    Arguments:
    - `connection`: string of host:port
    """

    def __init__(self, connection):
        """
        Create the zookeeper.client instance

        Arguments:
        - `connection`: string host:port
        """
        self.server = connection
        self._zk = None
        return

    def connect(self):
        """
        Create a connection to the ZooKeeper instance

        Return: None
        Exceptions: None
        """
        self._zk = zookeeper.init(self.server, self._eventhandler)

    def close(self):
        """
        Close the connection to our ZooKeeper instance

        Return: None
        Exceptions: None
        """
        if self._zk:
            zookeeper.close(self._zk)

    def _eventhandler(self, zk, etype, conn, path):
        """
        Callback for libzookeeper that fires when ZooKeeper events occur.

        Dispatch to our own callbacks.

        Arguments:
        - `zk`: handle to the ZooKeeper connection
        - `etype`: Enum- Event type
        - `conn`: Enum Connection Status
        - `path`: string- Path that the event occured

        Return: None
        Exceptions: None
        """
        pass

    def create(self, path, value='', acl=[OPEN_ACL_UNSAFE], flags=0):
        """
        Create a new Node at `path` containing `value` on our ZooKeeper instance.

        Arguments:
        - `path`: string - new path
        - `value`: string - value of the Node
        - `acl`: list - list of Access Control flags
        - `flags`: int - the ZooKeeper flags (SEQUENCE|EPHEMERAL)

        Return: None
        Exceptions: NodeExistsError
        """
        return zookeeper.create(self._zk, path, value, acl, flags)

    def get(self, path):
        """
        Get the value of the ZooKeeper Node at `path`

        Arguments:
        - `path`: string

        Return: Tuple of (Value, Statsdict)
        Exceptions: NoNodeError
        """
        return zookeeper.get(self._zk, path, None)

    def get_children(self, path):
        """
        Return a list of strings representing the child nodes of `path`

        Arguments:
        - `path`: string

        Return: list of strings
        Exceptions: NoNodeError
        """
        return zookeeper.get_children(self._zk, path, None)

    def exists(self, path):
        """
        Determine whether the ZooKeeper Node at `path` exists

        Arguments:
        - `path`: string

        Return: dict of stats or None
        Exceptions: None
        """
        return zookeeper.exists(self._zk, path, None)
