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
zoop.client
"""
from os.path import join
import threading

import zookeeper

from zoop import exceptions, watch

OPEN_ACL_UNSAFE = dict(perms=zookeeper.PERM_ALL, scheme = 'world', id='anyone')

class BaseZK(object):
    """
    Common ZooKeeper Client protocol for subclassing
    """
    flavour = 'Base Client'

    def __init__(self, connection):
        """
        Create the zookeeper.client instance

        Arguments:
        - `connection`: string host:port
        """
        self.connwait = 10.0
        self.connected = False
        self.cv = threading.Condition()
        self.server = connection
        self._zk = None
        self.watcher = watch.Watcher(self._zk)
        return

    def __repr__(self):
        return "<ZooKeeper {0} for {1}>".format(
            self.flavour, self.server)

    def connect(self):
        """
        Create a connection to the ZooKeeper instance

        Return: None
        Exceptions: None
        """
        def connwatch(handle, etype, state, path):
            with self.cv:
                self.connected = True
                self.cv.notify()
            return

        with self.cv:
            self._zk = zookeeper.init(self.server, connwatch)
            self.cv.wait(self.connwait)
            if not self.connected:
                raise Exception("!")

        self.watcher.set_zhandle(self._zk)
        self.watcher.set_global()


class ZooKeeper(BaseZK):
    """
    The ZooKeeper client

    Arguments:
    - `connection`: string of host:port

    Return: None
    Exceptions: None
    """
    flavour = 'Client'

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
        Exceptions:
        - NodeExistsError: This Node already exists
        - NoNodeError: A parent Node in `path` does not exist

        """
        try:
            return zookeeper.create(self._zk, path, value, acl, flags)
        except zookeeper.NodeExistsException:
            errstr = "Can't create {0} as it already exists".format(path)
            raise exceptions.NodeExistsError(errstr)
        except zookeeper.NoNodeException:
            errstr = "A parent node of {0} does not exist".format(path)
            raise exceptions.NoNodeError(errstr)

    def delete(self, path):
        """
        Delete the ZooKeeper Node at `path`

        Arguments:
        - `path`: string

        Return: None
        Exceptions: NoNodeError
        """
        try:
            zookeeper.delete(self._zk, path)
        except zookeeper.NoNodeException:
            errmsg = "The Node {0} does not exist".format(path)
            raise exceptions.NoNodeError(errmsg)

    def exists(self, path, watch=None):
        """
        Determine whether the ZooKeeper Node at `path` exists

        Arguments:
        - `path`: string

        Return: dict of stats or None
        Exceptions: None
        """
        return zookeeper.exists(self._zk, path, watch)

    def get(self, path, watch=None):
        """
        Get the value of the ZooKeeper Node at `path`

        Arguments:
        - `path`: string
        - `watch`: callable - optional watcher function

        Return: Tuple of (Value, Statsdict)
        Exceptions: NoNodeError
        """
        return zookeeper.get(self._zk, path, watch)

    def get_children(self, path):
        """
        Return a list of strings representing the child nodes of `path`

        Arguments:
        - `path`: string

        Return: list of strings
        Exceptions: NoNodeError
        """
        # !!! Wrap the ZooKeeper exceptions
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

    def mkdirp(self, path):
        """
        Recursively make all nodes in the given path

        Arguments:
        - `path`: string

        Return: None
        Exceptions: None
        """
        paths = path.split('/')
        for i, path in enumerate(paths):
            p = join(join(paths[:i]), path)
            if not self.exists(p):
                self.create(p)

    def set(self, path, value):
        """
        Set the value of the ZooKeeper Node at `path`

        Arguments:
        - `path`: string
        - `value`: string

        Return: None
        Exceptions: NoNodeError
        """
        zookeeper.set(self._zk, path, value)
        return

    def watch(self, path, callback, event):
        """
        Begin watching `path` for events of type `event`.
        When one happens, execute `callback`, with two
        arguments, the path of the ZooKeeper Even and the event type

        Arguments:
        - `path`: string - Path to watch
        - `callback`: callable
        - `event`: int - a zoop.Event attribute

        Return: None
        Exceptions: None
        """
        self.watcher.spyon(path, callback, event)
        return

    def Queue(self, path):
        """
        Returns an instantiated Queue with the root `path`
        connected to this ZooKeeper instance.

        Arguments:
        - `path`: string - the root of your Queue. should be an
                           absolute path.

        Return: Queue
        Exceptions: NotConnectedError - the ZooKeeper instance was not connected
        """
        if not self.connected:
            err = "You aren't connected to a ZooKeeper instance - no way to create a Queue"
            raise exceptions.NotConnectedError(err)
        # Avoid circular imports from the top-level package namespace
        from zoop import queue
        return queue.Queue(self, path)




class AsyncZooKeeper(object):
    """
    A ZooKeeper client that uses the Asynchronous
    libzookeeper API.

    Methods can be expected to take an additional
    callback parameter.
    """
    flavour = 'Async Client'
