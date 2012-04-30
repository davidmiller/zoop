"""
zoop.client
"""
import collections

import zookeeper

from zoop.enums import Event

OPEN_ACL_UNSAFE = dict(perms=zookeeper.PERM_ALL, scheme = 'world', id='anyone')

class Watcher(object):
    """
    Stores a register of callbacks for particular watchers.
    """
    def __init__(self, zkh):
        """
        Store vars

        Arguments:
        - `zkh`: zookeeper instance handle

        Return: None
        Exceptions: None
        """
        self._zk = zkh
        self.callbacks = collections.defaultdict(lambda: collections.defaultdict(list))

    def dispatch(self, zk, etype, conn, path):
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
        print "Got watch event", path, etype
        if self.callbacks[path][etype]:
            self.callbacks[path][etype](path, etype)
        return

    def spyon(self, path, event, callback):
        """
        Begin watching `path` for events of type `event`.
        When one happens, execute `callback`, with two
        arguments, the path of the ZooKeeper Event and the Event type.

        Arguments:
        - `path`: string - Path to watch
        - `event`: int - a zoop.Event attribute
        - `callback`: callable

        Return: None
        Exceptions: None
        """
        print "Start spying on", path
        self.callbacks[path][event].append(callback)
        #zookeeper.get(self._zk, path, self.dispatch)
        #zookeeper.get_children(self._zk, path, self.dispatch)
        return


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
        self.watcher = Watcher(self._zk)
        return

    def connect(self):
        """
        Create a connection to the ZooKeeper instance

        Return: None
        Exceptions: None
        """
        self._zk = zookeeper.init(self.server, None)
        self.watcher._zk = self._zk

    def close(self):
        """
        Close the connection to our ZooKeeper instance

        Return: None
        Exceptions: None
        """
        if self._zk:
            zookeeper.close(self._zk)

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

    def ls(self, path):
        """
        Return a list of strings representing the child nodes of `path`

        (Note, this is an alias of get_children)
        Arguments:
        - `path`: string

        Return: list of strings
        Exceptions: NoNodeError
        """
        return self.get_children(path)

    def exists(self, path):
        """
        Determine whether the ZooKeeper Node at `path` exists

        Arguments:
        - `path`: string

        Return: dict of stats or None
        Exceptions: None
        """
        return zookeeper.exists(self._zk, path, None)

    def set(self, path, value):
        """
        Set the value of the ZooKeeper Node at `path`

        Arguments:
        - `path`: string
        - `value`: string

        Return: Tuple of (Value, Statsdict)
        Exceptions: NoNodeError
        """
        return zookeeper.set(self._zk, path, value)

    def watch(self, path, event, callback):
        """
        Begin watching `path` for events of type `event`.
        When one happens, execute `callback`, with two
        arguments, the path of the ZooKeeper Even and the event type

        Arguments:
        - `path`: string - Path to watch
        - `event`: int - a zoop.Event attribute
        - `callback`: callable

        Return: None
        Exceptions: None
        """
        self.watcher.spyon(path, event, callback)
        return

