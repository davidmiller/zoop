"""
unittests for the zoop.lock module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock
import zookeeper

from zoop import lock

class BaseLockTestCase(unittest.TestCase):
    def setUp(self):
        self.zk = Mock(name='Mock ZooKeeper')
        self.lk = lock.BaseLock(self.zk, 'barlock')

    def test_init(self):
        """ Initializer """
        self.zk.exists.return_value = False

        lk = lock.BaseLock(self.zk, 'foolock', root='/lockz')
        self.assertEqual('/lockz/foolock', lk.path)
        self.zk.exists.assert_any_call('/lockz/foolock')
        self.zk.exists.assert_any_call('/lockz')
        self.zk.create.assert_any_call('/lockz/foolock')
        self.zk.create.assert_any_call('/lockz')

    def test_contextmanager(self):
        "Can we use it as a contextmanager?"
        with patch.object(self.lk, 'acquire') as Pac:
            with patch.object(self.lk, 'release') as Prel:
                with self.lk:
                    Pac.assert_called_once_with()
                Prel.assert_called_once_with()

    def test_revoked(self):
        """ Predicatise a list """
        self.lk.tlocal.revoked.append(True)
        self.assertEqual(True, self.lk.revoked)

    def test_not_revoked(self):
        """ We haven't been asked to revoke yet. """
        self.assertEqual(False, self.lk.revoked)

    def test_acquire(self):
        "Acquire the lock"
        # !!! This is brittle.
        self.zk.get.return_value = 'got'
        self.zk.create.return_value = '/lockz/foolock/lock-00000001'
        self.zk.get_children.return_value = ['lock-00000001']
        self.assertEqual(True, self.lk.acquire())

    def test_create_waitnode(self):
        "Create a wait node."
        self.zk.create.return_value = '/zooplocks/barlock/baselock-00000001'
        self.zk.get.return_value = 'got'

        nodepath, keynode = self.lk._create_waitnode()
        self.zk.create.assert_called_once_with('/zooplocks/barlock/baselock-',
                                               value = '0',
                                               flags = zookeeper.SEQUENCE)
        self.assertEqual('/zooplocks/barlock/baselock-00000001', nodepath)
        self.assertEqual('baselock-00000001', keynode)

    def test_has_lock(self):
        """ Do we have the lock """
        cases = [
            ((True, None), ('baselock-0001', ['baselock-0001', 'baselock-0002'])),
            ((False, ['baselock-0001']), ('baselock-0002', ['baselock-0001', 'baselock-0002']))
            ]
        for expected, arg in cases:
            actual = self.lk.has_lock(*arg)
            self.assertEqual(expected, actual)

    def test_release(self):
        "Can we release the lock?"
        self.assertEqual(True, self.lk.release())

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
