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
import threading

import zookeeper

from zoop import exceptions, watch

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
        self.connwait = 10.0
        self.connected = False
        self.cv = threading.Condition()
        self.server = connection
        self._zk = None
        self.watcher = watch.Watcher(self._zk)
        return

    def __repr__(self):
        return "<ZooKeeper Client for {0}>".format(self.server)

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
        try:
            return zookeeper.create(self._zk, path, value, acl, flags)
        except zookeeper.NodeExistsException:
            errstr = "Can't create {0} as it already exists".format(path)
            raise exceptions.NodeExistsError(errstr)

    def delete(self, path):
        """
        Delete the ZooKeeper Node at `path`

        Arguments:
        - `path`: string

        Return: None
        Exceptions: None
        """
        zookeeper.delete(self._zk, path)

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

class AsyncZooKeeper(object):
    """
    A ZooKeeper client that uses the Asynchronous
    libzookeeper API.

    Methods can be expected to take an additional
    callback parameter.
    """
