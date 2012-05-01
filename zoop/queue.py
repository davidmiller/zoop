"""
zoop.queue

Distributed Queue implementation running on Zookeeper.

As much as is possible this implementation seeks to mirror the API
established by the Standard Library's queue module.
"""

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

    def __repr__(self):
        return "<ZooKeeper FIFO Queue at {0}{1}>".format(self.zk.server, self.path)

    def empty(self):
        """
        Return ``True`` if the queue is empty, False otherwise.

        Return: bool
        Exceptions: None
        """
        raise NotImplementedError()

    def get(self):
        """
        Return the next item from the Queue

        Return: string data item
        Exceptions: Empty
        """
        raise NotImplementedError()

    def put(self, item):
        """
        Put `item` at the end of the queue.

        Arguments:
        - `item`: string - data to add

        Return: None
        Exceptions: None
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        >>> myq = Queue(zk, '/myq')
        >>> def watchit(data):
        ...     print "Watchit got", data, "!"
        >>> assert(callable(watchit))
        >>> myq.watch(watchit)
        >>> myq.put("Frist")
        Watchit got "Frist" !
        """
        raise NotImplementedError()
