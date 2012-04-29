"""
unittests for the zoop.client module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch

from zoop import client

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
            self.assertEqual(None, self.zk._zk)
            self.zk.connect()
            Pinit.assert_called_once_with('localhost:2181', self.zk._eventhandler)
            self.assertEqual(Pinit.return_value, self.zk._zk)


if __name__ == '__main__':
    unittest.main()
