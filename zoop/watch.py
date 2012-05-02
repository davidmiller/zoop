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
zoop.watcher

Callbacks for state change go here!
"""
import collections
import threading

PLock = threading.RLock()

import zookeeper

from zoop import enums, exceptions

class Watcher(object):
    """
    Stores a register of callbacks for particular watchers.

    >>> zk = zookeeper.init('localhost:2181)
    >>> watcher = Watcher(zk)
    >>> def cb(event, path):
    ...     print 'Got Called!", path, event
    ...
    >>> watcher.spyon('/zookeeper', cb, Event.Child)
    >>> client = Client('localhost:2181')
    >>> client.create('/zookeeper/yay', 'Hello Beautiful World')
    ... Got Called! /zookeeper/yay 4
    """

    _watch_funcs = {
        enums.Event.Deleted: zookeeper.get,
        enums.Event.Changed: zookeeper.get,
        enums.Event.Child: zookeeper.get_children
        }

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

    def set_global(self):
        """
        Set our dispatch function as the ZooKeeper global watcher.

        Return: None
        Exceptions: None
        """
        zookeeper.set_watcher(self._zk, self.dispatch)
        return

    def dispatch(self, zk, etype, conn, path):
        """
        Callback for libzookeeper that fires when ZooKeeper events occur.

        Dispatch to our own callbacks.
        Then re-watch the node/event type

        Arguments:
        - `zk`: handle to the ZooKeeper connection
        - `etype`: Enum- Event type
        - `conn`: Enum Connection Status
        - `path`: string- Path that the event occured

        Return: None
        Exceptions: None

        """
        if etype == enums.Event.Session:
            return

        if etype in self._watch_funcs:
            self._watch_funcs[etype](self._zk, path, self.dispatch)

        if self.callbacks[path][etype] > 0:
            for cb in self.callbacks[path][etype]:
                cb(path, etype)

        def watchit(h, t, s, p):
            self.dispatch(h, t, s, p)

        return

    def spyon(self, path, callback, *events):
        """
        Begin watching `path` for events of type `event`.
        When one happens, execute `callback`, with two
        arguments, the path of the ZooKeeper Event and the Event type.

        Arguments:
        - `path`: string - Path to watch
        - `callback`: callable
        - `*events`: int - one or more zoop.Event attribute. Must pass
                           at least one

        Return: None
        Exceptions:
        - NoEventError: No events passed.
        """
        if not events: # Valid syntax, but invalid semantics
            errmsg = "You must pass at least one Event to spy on"
            raise exceptions.NoEventError(errmsg)
        for e in events:
            self.callbacks[path][e].append(callback)

            def cb(h, t, s, p):
                self.dispatch(h, t, s, p)
                return

            print self._watch_funcs[e](self._zk, path, cb)
        return
