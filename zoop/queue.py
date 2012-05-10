# Copyright (c) 2012 David Miller (david@deadpansincerity.com)
#
# This file is part of zoop (http://github.com/davidmiller/zoop)
#
# zoop is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
zoop.queue

Distributed Queue implementation running on Zookeeper.

As much as is possible this implementation seeks to mirror the API
established by the Standard Library's queue module.

"""
import os

import zookeeper

from zoop import enums, exceptions, lock

class Queue(object):
    """
    A FIFO queue for ZooKeeper.

    Specifying the prefix allows you interoperability with
    Queue implementations from other libraries.

    Arguments:
    - `client`: ZooKeeper
    - `path`: string Path we want to treat as a queue
    - `prefix`: prefix string for the item nodes.

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
    def __init__(self, client, path, prefix='q-'):
        self.zk = client
        self.path = path
        self.prefix = prefix
        if not self.zk.exists(path):
            self.zk.create(path)
        name = os.path.basename(path) + '-lock'
        self.lock = lock.Lock(client, name, os.path.dirname(path))

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
        Watch the Queue for items being added, and when they are,
        call `callback` with a list of items currently in the Queue.

        `callback` should be a callable that takes a single argument.
        It should expect a list of strings.

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
        Watchit got ['q-00000001'] !
        """
        def watcher(event, path):
            """
            Watch for items added to the Queue, then remove the latest and
            run the callback on it.
            """
            try:
                kids = self.sorted()
            except exceptions.Empty:
                return # Deleted event
            return callback(kids)

        self.zk.watch(self.path, watcher, enums.Event.Child)
        return

    def watchitem(self, callback):
        """
        Watch for items being added to the queue, and call
        callback with the contents of added nodes when they
        are added.

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
        >>> myq.watchitem(watchit)
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



"""
!!! PriorityQueue

To implement a priority queue, you need only make two simple changes
to the generic queue recipe . First, to add to a queue, the pathname
ends with "queue-YY" where YY is the priority of the element with lower
numbers representing higher priority (just like UNIX). Second, when
removing from the queue, a client uses an up-to-date children list
meaning that the client will invalidate previously obtained children
lists if a watch notification triggers for the queue node.
"""
