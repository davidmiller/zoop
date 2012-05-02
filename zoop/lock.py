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
import os

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
        self.path = os.path.join(root, name)
        if not self.zk.exists(root):
            self.zk.create(root)
        if not self.zk.exists(self.path):
            self.zk.create(self.path)
        return

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
        return


class Lock(object):
    """
    Synchronise your lockage!
    """
    prefix = 'lock-'
