"""
Unittests for the zoop.watch module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock

import zoop
from zoop import enums, exceptions, watch

class WatcherTestCase(unittest.TestCase):
    def setUp(self):
        self.w = watch.Watcher(2)
        self.mock_callback = Mock(name='Mock Callback')

    def test_sethandle(self):
        "Attribute setter for interface"
        mock_handle = Mock(name='Mock Handle')
        self.w.set_zhandle(mock_handle)
        self.assertTrue(self.w._zk is mock_handle)

    def test_dispatch(self):
        """ Run our callbacks and reregister them """
        cb = Mock(name='Mock Callback')
        mock_kids = Mock(name='Mock get_children()')
        values = {enums.Event.Child: mock_kids}
        self.w.callbacks['/foo/bar'][enums.Event.Child].append(cb)
        with patch.dict(watch.Watcher._watch_funcs, values):
            self.w.dispatch(2, enums.Event.Child, None, '/foo/bar')
            cb.assert_called_once_with('/foo/bar', enums.Event.Child)
            args = mock_kids.call_args[0]
            self.assertEqual(self.w._zk, args[0])
            self.assertEqual('/foo/bar', args[1])

    def test_spyon_no_events(self):
        """ Raise when no events passed """
        with self.assertRaises(exceptions.NoEventError):
            self.w.spyon('/joo/kar', self.mock_callback)

    def test_spyon_child(self):
        """ Register our desire to watch for events """
        cb = lambda *a,**k: True
        mock_kids = Mock(name='Mock get_children()')
        values = {enums.Event.Child: mock_kids}
        with patch.dict(watch.Watcher._watch_funcs, values):
            self.w.spyon('/foo/bar', cb, zoop.Event.Child)
            self.assertEqual([cb], self.w.callbacks['/foo/bar'][zoop.Event.Child])
            args = mock_kids.call_args[0]
            self.assertEqual(self.w._zk, args[0])
            self.assertEqual('/foo/bar', args[1])

    def test_spyon_changed(self):
        """ Register our desire to watch for events """
        cb = lambda *a,**k: True
        mock_get = Mock(name='Mock get()')
        values = {
            enums.Event.Changed: mock_get,
            enums.Event.Deleted: mock_get
            }

        with patch.dict(watch.Watcher._watch_funcs, values):
            self.w.spyon('/foo/bar', cb, zoop.Event.Changed, zoop.Event.Deleted)
            self.assertEqual([cb], self.w.callbacks['/foo/bar'][zoop.Event.Changed])
            self.assertEqual([cb], self.w.callbacks['/foo/bar'][zoop.Event.Deleted])
            args = mock_get.call_args[0]
            self.assertEqual(self.w._zk, args[0])
            self.assertEqual('/foo/bar', args[1])



if __name__ == '__main__':
    unittest.main()
