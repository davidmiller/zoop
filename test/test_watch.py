"""
Unittests for the zoop.watch module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock

from zoop import watch

class WatcherTestCase(unittest.TestCase):
    def setUp(self):
        self.w = watch.Watcher(None)

    def test_sethandle(self):
        "Attribute setter for interface"
        mock_handle = Mock(name='Mock Handle')
        self.w.set_zhandle(mock_handle)
        self.assertTrue(self.w._zk is mock_handle)


    def test_spyon(self):
        """ Register our desire to watch for events """
        #cb = lambda *a,**k: True
        # self.w.spyon('/foo/bar', zoop.Event.Child, cb)
        # self.assertEqual([cb], self.w.callbacks['/foo/bar'][zoop.Event.Child])
        # !!! Make this a real test please!

if __name__ == '__main__':
    unittest.main()
