.. _installation:

============
Installation
============

Let's get installed!

Dependencies
============

Zoop relies on the Python bindings to *libzookeeper* under the hood, so the
first step is probably to get that installed.

Via Your Package Manager
------------------------

Many modern linux distributions will come with a package for the Python bindings
to libzookeeper - for example, on Debian based distros one would simply::

    $ apt-get install python-zookeeper

Pip
---

Alternatively, you can Pip install the package `zc-zookeeper-static`_ which is a self-contained
statically built distribution with::

   $ pip install zc-zookeeper-static

.. _`zc-zookeeper-static`: http://pypi.python.org/pypi/zc-zookeeper-static


Installing Zoop itself
======================

The easiest wat to install zoop is via `pip`_::

    $ pip install zoop

.. _`pip`: http://www.pip-installer.org


Use The Source
--------------

You can also install zoop by getting yourself a copy of the `source`_ if you have git installed::

    $ git clone git://github.com/davidmiller/zoop

.. _`source`: https://github.com/davidmiller/zoop

Installing ZooKeeper
====================

How to install ZooKeeper is beyond the scope of this document, but please consult the excellent installation details at http://zookeeper.apache.org/