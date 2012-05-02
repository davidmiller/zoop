"""
unittests for the zoop.client module
"""
import os
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import Mock
import zookeeper

from zoop import exceptions, queue

class QueueTestCase(unittest.TestCase):
    def setUp(self):
        self.zk = Mock(name='Mock ZooKeeper')
        self.q = queue.Queue(self.zk, '/foo/q')

    def test_init_exists(self):
        "Don't create, it exists"
        zk = Mock(name='Mock ZooKeeper')
        zk.exists.return_value = True
        queue.Queue(zk, '/bar/q')
        zk.exists.assert_called_once_with('/bar/q')

    def test_init_doesnt_exist(self):
        "Don't create, it exists"
        zk = Mock(name='Mock ZooKeeper')
        zk.exists.return_value = False
        queue.Queue(zk, '/bar/q')
        zk.exists.assert_called_once_with('/bar/q')
        zk.create.assert_called_once_with('/bar/q')

    def test_empty(self):
        """ The queue is empty """
        self.zk.get_children.return_value = []
        self.assertEqual(True, self.q.empty())

    def test_not_empty(self):
        """ The Queue is not empty """
        self.zk.get_children.return_value = ['q-1', 'q-2']
        self.assertEqual(False, self.q.empty())

    def test_flush(self):
        "Flush a Q"
        nodes = ['q-1', 'q-2']
        self.zk.get_children.return_value = nodes
        self.q.flush()
        self.zk.get_children.assert_called_once()
        for n in nodes:
            self.zk.delete.assert_any_call(os.path.join('/foo/q', n))

    def test_get(self):
        """ Take the next element from the Queue"""
        self.zk.get_children.return_value = ['q-1', 'q-2']
        self.zk.get.return_value = 'Q1 Data'

        self.assertEqual("Q1 Data", self.q.get())

        self.zk.get_children.assert_called_once_with('/foo/q')
        self.zk.get.assert_called_once_with('/foo/q/q-1')
        self.zk.delete.assert_called_once_with('/foo/q/q-1')

    def test_get_empty(self):
        "The Queue is empty, raise an Empty error"
        self.zk.get_children.return_value = []
        with self.assertRaises(exceptions.Empty):
            self.q.get()

    def test_put(self):
        """ Put an item into the Queue """
        self.q.put('Foo')
        self.zk.create.assert_called_once_with('/foo/q/q-', value='Foo', flags=zookeeper.SEQUENCE)

    def test_qsize(self):
        "Length of the Q"
        self.zk.get_children.return_value = ['q-1']
        self.assertEqual(1, self.q.qsize())

    def test_sorted(self):
        """ Get the sorted list of items """
        self.zk.get_children.return_value = ['q-2', 'q-4', 'q-3']
        self.assertEqual(['q-2', 'q-3', 'q-4'], self.q.sorted())

    def test_sorted_empty(self):
        self.zk.get_children.return_value = []
        with self.assertRaises(exceptions.Empty):
            self.q.sorted()

    def test_watch(self):
        cb = Mock(name='Mock Callback')
        self.q.watch(cb)
        self.zk.watch.assert_called_once()

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
