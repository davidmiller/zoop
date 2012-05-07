"""
unittests for the zoop.client module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock
import zookeeper

import zoop
from zoop import client, exceptions, logutils, queue

logutils.set_loglevel('ERROR')

class BaseZKTestCase(unittest.TestCase):
    def setUp(self):
        self.zk = client.BaseZK('localhost:2181')

    def test_init(self):
        """ store vars """
        self.assertEqual('localhost:2181', self.zk.server)
        self.assertEqual(None, self.zk._zk)

    def test_connect(self):
        """ Connect to the Zookeeper instance """
        self.zk.connwait = 0.1

        with patch.object(client.zookeeper, 'init') as Pinit:

            def connected(server, handler, *args):
                handler(1, -1, 1, None)
                return 1

            Pinit.side_effect = connected
            with patch.object(self.zk, 'watcher'):
                self.assertEqual(None, self.zk._zk)
                self.zk.connect()
                Pinit.assert_called_once()
                self.assertEqual(1, self.zk._zk)
                self.assertEqual(True, self.zk.connected)


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.zk = client.ZooKeeper('localhost:2181')

    def test_create(self):
        """ Create a node """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.create('/foo/bar', 'YAY')
            self.assertEqual(Pzk.create.return_value, resp)
            Pzk.create.assert_called_once_with(self.zk._zk, '/foo/bar', 'YAY',
                                               [client.OPEN_ACL_UNSAFE], 0)

    def test_create_exists(self):
        """ Raise if it exists """
        def raiser(*a, **k):
            raise(zookeeper.NodeExistsException("!"))

        with patch.object(client.zookeeper, 'create') as Pcreate:
            Pcreate.side_effect = raiser
            with self.assertRaises(exceptions.NodeExistsError):
                self.zk.create('/exists')

    def test_delete(self):
        """ Delete a node """
        with patch.object(client, 'zookeeper') as Pzk:
            self.zk.delete('/foo/bar')
            Pzk.delete.assert_called_once_with(self.zk._zk, '/foo/bar')

    def test_delete_no_node(self):
        """ Delete a node """
        def raiser(*a,**kw):
            raise(zookeeper.NoNodeException("!"))

        with patch.object(client.zookeeper, 'delete') as Pdel:
            Pdel.side_effect = raiser

            with self.assertRaises(exceptions.NoNodeError):
                self.zk.delete('/foo/bar')
                Pdel.assert_called_once_with(self.zk._zk, '/foo/bar')

    def test_get(self):
        """ Should Make a get request to libzookeeper """
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.get('/foo/bar')
            self.assertEqual(Pzk.get.return_value, resp)
            Pzk.get.assert_called_once_with(self.zk._zk, '/foo/bar', None)

    def test_get_watch(self):
        """ Should Make a get request to libzookeeper """
        with patch.object(client, 'zookeeper') as Pzk:
            watch = Mock(name='Mock Watch')
            resp = self.zk.get('/foo/bar', watch)
            self.assertEqual(Pzk.get.return_value, resp)
            Pzk.get.assert_called_once_with(self.zk._zk, '/foo/bar', watch)


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

    def test_exists_watch(self):
        """ Should Make an exists request to libzookeeper """
        cb = Mock(name='Mock Callback')
        with patch.object(client, 'zookeeper') as Pzk:
            resp = self.zk.exists('/foo/bar', watch=cb)
            self.assertEqual(Pzk.exists.return_value, resp)
            Pzk.exists.assert_called_once_with(self.zk._zk, '/foo/bar', cb)

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

    def test_queue_no_connection(self):
        """ Should raise an error """
        with self.assertRaises(exceptions.NotConnectedError):
            self.zk.Queue('/myq')

    def test_queue(self):
        self.zk.connected = True
        with patch.object(queue, 'Queue') as Pq:
            q = self.zk.Queue('/myq')
            Pq.assert_called_once_with(self.zk, '/myq')




if __name__ == '__main__':
    unittest.main()
