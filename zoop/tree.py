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
zoop.tree

Representing ZooKeeper Node trees.

>>> t = Tree()
>>> t.add_nodes('/foo/bar/goo/car')
"""
class Tree(object):
    def __init__(self):
        self.nodes = {}

    def __repr__(self):
        return "<zoop Tree>"

    @staticmethod
    def from_zk(zk, root='/', level=None, pattern=None, exclude=None):
        """
        Inspect the ZooKeeper instance connected in `zk, and create a
        tree representing the schema starting at `root`, and descending
        `level` subdirectories.

        If the `pattern` argument is passed, only include those Nodes whose
        name matches the regexp `pattern`.

        If the `exclude` argument is passed, exclude any Nodes whose name
        matches the regexp `exclude`

        Arguments:
        - `zk`: ZooKeeper
        - `root`: str - the node to start at.
        - `level`: int - the number of child Nodes to descend.
        - `pattern`: str - regexp
        - `exclude`: str - regexp

        Return: Tree
        Exceptions: None
        """
        return Tree()

    def add_nodes(self, path, nodes):
        # This is very possibly not the API you are looking for
        pathlist = [p for p in path.split('/') if p]
        print pathlist
        current = self.nodes
        for path in pathlist:
            if not path in current or current[path] == None:
                current[path] = {}
            current = current[path]
        for n in nodes:
            current[n] = None

    def tree(self):
        """
        Return a string representation of the Nodes
        in this ZooKeeper Instance

        Return: str
        Exceptions: None
        """
        lines = ['/']

        def rectree(nodes, prefix):
            nodenames = sorted(nodes.keys())
            for i, child in enumerate(nodenames):
                lines.append('{0}|-- {1}'.format(prefix, child))
                if nodes[child]:
                    nodefix = ' ' * 4
                    if i + 1 < len(nodenames):
                        nodefix = '|{0}'.format(nodefix[1:])
                    subfix = '{0}{1}'.format(prefix, nodefix)
                    rectree(nodes[child], subfix)

        rectree(self.nodes, ' ')
        return "\n".join(lines)

    def pprint(self):
        """
        Print a string representation of the Nodes
        in this ZooKeeper Instance

        Return: None
        Exceptions: None
        """
        print self.tree()
        return

