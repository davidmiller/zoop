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
zoop.lock

A distributed Lock on top of ZooKeeper
"""
from os.path import join
import threading
import time

import zookeeper

from zoop import exceptions

class BaseLock(object):
    """
    A base for all subsequent locks to inherit from.
    """
    prefix = 'baselock-'

    def __init__(self, handle, name, root='/zooplocks'):
        """
        Store instance vars and ensure that the Node exists

        Arguments:
        - `handle`: ZooKeeper
        - `name`: str
        - `root`: str

        Return: None
        Exceptions: None
        """
        self.zk = handle
        self.name = name
        self.root = root
        self.path = join(root, name)
        self.tlocal = threading.local()
        self.tlocal.revoked = []
        self.tlocal.locking = None
        if not self.zk.exists(root):
            self.zk.create(root)
        if not self.zk.exists(self.path):
            self.zk.create(self.path)
        return

    def __repr__(self):
        return "<BaseLock for {0}>".format(self.path)

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    @property
    def revoked(self):
        """
        Predicate to indicate whether we have been asked to
        release this lock.

        Returns: bool
        Exceptions: None
        """
        return bool(self.tlocal.revoked)

    def acquire(self, timeout=None):
        """
        Attempt to acquire the lock.

        If a timeout parameter is passed, only wait this long
        for acquisition.

        Arguments:
        - `timeout`: int

        Return: None
        Exceptions: None
        """
        # This implementation is based upon the Mozilla Services
        # ztools lock at https://github.com/mozilla-services/zktools
        self.tlocal.revoked = []

        nodepath, keyname = self._create_waitnode()

        acquired = False
        cv = threading.Event()

        def lockwatch(handle, etype, state, path):
            cv.set()

        tstart = time.time()

        while not acquired:
            cv.clear()

            if timeout is not None and time.time() - tstart > timeout:
                try:
                    self.zk.delete(nodepath)
                except exceptions.NoNodeError:
                    pass
                return False

            kids = self.zk.get_children(self.path)
            # This sort isn't used here, but in has_lock()
            kids.sort(key=lambda val: val[val.rfind('-') + 1:])

            if len(kids) == 0 or not keyname in kids:
                # Only really for connection issues
                nodepath, keyname = self._create_waitnode()
                continue

            acquired, blocking = self.has_lock(keyname, kids)
            if acquired:
                break

            last_blocker = join(self.path, blocking[-1])
            if not self.zk.exists(last_blocker, lockwatch):
                continue # Wait - what?

            if timeout is not None:
                cv.wait(timeout - (time.time() - tstart))

        self.tlocal.lock_node = nodepath
        return

    def _create_waitnode(self):
        """
        Create the wait node for our thread.
        When this is the lowest number, we have the lock.

        Return: tuple of strings -
               * Full path of the child
               * The nodename of the child
        Exceptions: None
        """

        def revoked(handle, etype, conn, path):
            removes = [zookeeper.DELETED_EVENT, zookeeper.EXPIRED_SESSION_STATE]
            if etype in removes:
                try:
                    self.tlocal.revoked.append(True)
                except AttributeError:
                    pass # We've already unlocked
                return

            if etype == zookeeper.CHANGED_EVENT:
                data = self.zk.get(path, revoked)
                if data == 'unlock':
                    try:
                        self.tlocal.revoked.append(True)
                    except AttributeError:
                        pass # We've already unlocked
            return

        nodepath = self.zk.create(join(self.path, self.prefix), value="0",
                                  flags=zookeeper.SEQUENCE)
        data = self.zk.get(nodepath, watch=revoked)[0]
        if data == 'unlock':
            self.tlocal.revoked.append(True)

        keyname = nodepath.split('/')[-1]
        return nodepath, keyname

    def has_lock(self, keypath, locknodes):
        """
        Determine whether the current Thread has the Lock.
        Look to see whether we're frist in the current locknodes.

        If we are, then great! - we have achieved Lock-varna.

        Otherwise, all locknodes before ours are blocking us :(

        Arguments:
        - `keypath`: string - this thread's node
        - `locknodes`: list of strings all wait nodes

        Return: tuple of (bool, list or None)
                we return a boolean which represents whether or
                not we have the lock, and a list of blocking Nodes
                or None.
        Exceptions: None
        """
        if keypath == locknodes[0]:
            return True, None
        return False, locknodes[:locknodes.index(keypath)]

    def release(self):
        """
        Release a Lock!

        Return: None
        Exceptions: None
        """
        self.tlocal.revoked = []
        try:
            self.zk.delete(self.tlocal.lock_node)
            del self.tlocal.lock_node
        except (zookeeper.NoNodeException, AttributeError):
            pass # We never had the Lock!
        return

class Lock(BaseLock):
    """
    Synchronise your lockage!

    >>> zk = ZooKeeper('localhost:2181')
    >>> zk.connect()
    >>> lk = Lock(zk, 'mylock')
    >>> with lk:
    ...     print zk.get_children('/zooplocks/mylock')
    ...
    ['lock-0000001']
    >>> zk.get_children('/zooplocks/mylock')
    []
    """
    prefix = 'lock-'
