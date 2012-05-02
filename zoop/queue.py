"""
zoop.queue

Distributed Queue implementation running on Zookeeper.

As much as is possible this implementation seeks to mirror the API
established by the Standard Library's queue module.
"""
import os

import zookeeper

from zoop import enums, exceptions

class Queue(object):
    """
    A FIFO queue for ZooKeeper

    Arguments:
    - `client`: ZooKeeper
    - `path`: string Path we want to treat as a queue

    >>> zk = ZooKeeper('localhost:2181')
    >>> myq = Queue(zk, '/myq')
    >>> myq.put("Frist")
    >>> myq.put("Next")
    >>> myq.get()
    "Frist"
    >>> myq.get()
    "Next"
    >>> myq.get()
    Traceback (most recent call last):
        ...
    Empty: No items in queue at /myq
    """
    def __init__(self, client, path):
        self.zk = client
        self.path = path
        self.prefix = 'q-'

    def __repr__(self):
        return "<ZooKeeper FIFO Queue at {0}{1}>".format(self.zk.server, self.path)

    def empty(self):
        """
        Return ``True`` if the queue is empty, False otherwise.
        Note, empty() == False does not guarantee that a subsequent
        get() will not raise an Empty error.

        Return: bool
        Exceptions: None
        """
        return len(self.zk.get_children(self.path)) == 0

    def flush(self):
        """
        Flush the Queue's current state, deleting all nodes.

        Return: None
        Exceptions: None
        """
        kids = self.zk.get_children(self.path)
        for k in kids:
            self.zk.delete(os.path.join(self.path, k))
        return

    def get(self):
        """
        Return the next item from the Queue

        Return: string data item
        Exceptions: Empty
        """
        frist = self.sorted()[0] # This can raise Empty()
        ipath = os.path.join(self.path, frist)
        item = self.zk.get(ipath)
        self.zk.delete(ipath)
        return item

    def put(self, item):
        """
        Put `item` at the end of the queue.

        Arguments:
        - `item`: string - data to add

        Return: None
        Exceptions: None
        """
        return self.zk.create(os.path.join(self.path, self.prefix),
                              value=item,
                              flags=zookeeper.SEQUENCE)

    def qsize(self):
        """
        Return the size of the queue.
        Note, qsize() > 0 doesn't guarantee that a subsequent
        get() will not raise an Empty error.

        The watch() API is the recommended way to consume items
        from a queue.

        Return: int
        Exceptions: None
        """
        return len(self.zk.get_children(self.path))

    def sorted(self):
        """
        Return the items in the Queue, sorted by time added

        Return: list containing strings
        Exceptions: Empty
        """
        contents = self.zk.get_children(self.path)
        if not contents:
            raise exceptions.Empty("Queue at {0} has no items".format(self.path))
        return sorted(contents)

    def watch(self, callback):
        """
        Watch for items being added to the queue, and call
        callback when they are added.

        Callback should be callable and should take one
        argument, the data for the item that has just been
        added to the queue.

        Arguments:
        - `callback`: callable

        Return: None
        Exceptions: None

        >>> zk = ZooKeeper('localhost:2181')
        >>> zk.connect()
        >>> myq = Queue(zk, '/myq')
        >>> def watchit(data):
        ...     print "Watchit got", data, "!"
        >>> assert(callable(watchit))
        >>> myq.watch(watchit)
        >>> myq.put("Frist")
        Watchit got "Frist" !
        """
        def watcher(event, path):
            """
            Watch for items added to the Queue, then remove the latest and
            run the callback on it.
            """
            try:
                data, stats = self.get()
            except exceptions.Empty:
                return # Deleted event
            return callback(data)

        self.zk.watch(self.path, watcher, enums.Event.Child)
