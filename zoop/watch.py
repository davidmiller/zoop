"""
zoop.watcher

Callbacks for state change go here!
"""
import collections

import zookeeper

class Watcher(object):
    """
    Stores a register of callbacks for particular watchers.

    >>> zk = zookeeper.init('localhost:2181)
    >>> watcher = Watcher(zk)
    >>> def cb(event, path):
    ...     print 'Got Called!", path, event
    ...
    >>> watcher.spyon('/zookeeper', Event.Child, cb)
    >>> client = Client('localhost:2181')
    >>> client.create('/zookeeper/yay', 'Hello Beautiful World')
    ... Got Called! /zookeeper/yay 4
    """

    __register_watches = [
        zookeeper.get,
        zookeeper.get_children
        ]

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

    def set_zhandle(self, handle):
        """
        Attribute setter for the watcher's active handle
        to a ZooKeeper instance.

        Although this is passed in at instantiation, we also
        sometimes want an interface to change the handle,
        without having calling code understand the internal
        implementation details of the Watcher class.

        Arguments:
        - `handle`: ZooKeeper instance handle

        Return: None
        Exceptions: None
        """
        self._zk = handle
        return

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
        #self.callbacks[path][event].append(callback)
        #zookeeper.get(self._zk, path, self.dispatch)
        #zookeeper.get_children(self._zk, path, self.dispatch)
        return
