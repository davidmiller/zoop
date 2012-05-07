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
>>> t.mkdirp('/foo/bar/goo/car')
"""
class Tree(object):
    def __init__(self):
        self.nodes = {}

    def __repr__(self):
        return "<zoop Tree>"

    def add_nodes(self, path, nodes):
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

        def rectree(nodes, indent):
            for child in sorted(nodes.keys()):
                lines.append('{0}|-- {1}'.format(' ' * indent, child))
                if nodes[child]:
                    rectree(nodes[child], indent + 4)

        rectree(self.nodes, 0)
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

