"""
unittests for the zoop.lock module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import Mock

from zoop import lock

class BaseLockTestCase(unittest.TestCase):
    def setUp(self):
        self.zk = Mock(name='Mock ZooKeeper')
        self.lk = lock.BaseLock(self.zh, 'barlock')

    def test_init(self):
        """ Initializer """
        self.zk.exists.return_value = False

        lk = lock.BaseLock(self.zk, 'foolock', root='/lockz')
        self.assertEqual('/lockz/foolock', lk.path)
        self.zk.exists.assert_any_call('/lockz/foolock')
        self.zk.exists.assert_any_call('/lockz')
        self.zk.create.assert_any_call('/lockz/foolock')
        self.zk.create.assert_any_call('/lockz')

    def test_acquire(self):
        "Acquire the lock"
        self.lk.acquire()
        self.zk.create.assert_called_once_with('/lockz/barlock/baselock-')

class LockTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        """ Initializer """
        pass

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
