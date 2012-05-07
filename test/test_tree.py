"""
Unittests for the zoop.tree module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch

from zoop import tree

SIMPLE_TREE = """/
|-- foo
    |-- bar
    |-- car
|-- goo"""

class TreeTestCase(unittest.TestCase):
    def setUp(self):
        self.t = tree.Tree()

    def test_add_nodes(self):
        """ Add nodes to a path """
        expected = {
            'foo': {
                'bar': {
                    'goo': None,
                    'car': None
                    }
            }}
        self.t.add_nodes('/foo/bar', ['goo', 'car'])
        self.assertEqual(expected, self.t.nodes)

    def test_simple_tree(self):
        """ Stringify ourselves. """
        self.t.nodes = {
            'foo': {
                'bar': None,
                'car': None
                },
            'goo': None
            }
        self.assertEqual(SIMPLE_TREE, self.t.tree())

    def test_pprint(self):
        "Test our Printing"
        with patch.object(self.t, 'tree') as Psc:
            Psc.return_value = ''
            self.t.pprint()
            Psc.assert_called_once_with()

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
