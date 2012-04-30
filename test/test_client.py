"""
unittests for the zoop.client module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch
import zookeeper

import zoop
from zoop import client, exceptions

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.zk = client.ZooKeeper('localhost:2181')

    def test_init(self):
        """ store vars """
        self.assertEqual('localhost:2181', self.zk.server)
        self.assertEqual(None, self.zk._zk)

    def test_connect(self):
        """ Connect to the Zookeeper instance """
        with patch.object(client.zookeeper, 'init') as Pinit:
            with patch.object(self.zk, 'watcher'):
                self.assertEqual(None, self.zk._zk)
                self.zk.connect()
                Pinit.assert_called_once_with('localhost:2181', None)
                self.assertEqual(Pinit.return_value, self.zk._zk)

    def test_create(self):
        """ Create a node """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.create('/foo/bar', 'YAY')
            self.assertEqual(Pzk.create.return_value, resp)
            Pzk.create.assert_called_once_with(self.zk._zk, '/foo/bar', 'YAY', [client.OPEN_ACL_UNSAFE], 0)

    def test_create_exists(self):
        """ Raise if it exists """
        def raiser(*a, **k):
            raise(zookeeper.NodeExistsException("!"))

        with patch.object(client.zookeeper, 'create') as Pcreate:
            Pcreate.side_effect = raiser
            with self.assertRaises(exceptions.NodeExistsError):
                self.zk.create('/exists')

    def test_get(self):
        """ Should Make a get request to libzookeeper """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.get('/foo/bar')
            self.assertEqual(Pzk.get.return_value, resp)
            Pzk.get.assert_called_once_with(self.zk._zk, '/foo/bar', None)

    def test_get_children(self):
        """ Should Make a get_children request to libzookeeper """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.get_children('/foo/bar')
            self.assertEqual(Pzk.get_children.return_value, resp)
            Pzk.get_children.assert_called_once_with(self.zk._zk, '/foo/bar', None)

    def test_exists(self):
        """ Should Make an exists request to libzookeeper """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.exists('/foo/bar')
            self.assertEqual(Pzk.exists.return_value, resp)
            Pzk.exists.assert_called_once_with(self.zk._zk, '/foo/bar', None)

    def test_ls(self):
        """ Replicate ls """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.ls('/goo/car')
            Pzk.get_children.assert_called_once_with(self.zk._zk, '/goo/car', None)
            self.assertEqual(Pzk.get_children.return_value, resp)

    def test_watch(self):
        """ Register our desire to watch for events """
        cb = lambda *a,**k: True
        with patch.object(self.zk.watcher, 'spyon') as Pspy:
            self.zk.watch('/foo/bar', zoop.Event.Child, cb)
            Pspy.assert_called_once_with('/foo/bar', zoop.Event.Child, cb)




if __name__ == '__main__':
    unittest.main()
