Zoop - ZooKeeper for Python!
============================

`Zookeeper`_ is a highly reliable distributed coordination service.

*Zoop* gives you a Pythonic API for accessing ZooKeeper instances, as well as
implementations of some common ZooKeeper patterns. This leaves you free to
concentrate on whatever it was you were originally doing::

    >>> zk =  zoop.ZooKeeper('localhost:2181')
    >>> zk.connect()
    >>> q = zoop.Queue(zk, '/howdy')
    >>> def gotit(data):
    ...     print "Gotit got data:", data
    >>> q.watch(gotit)
    >>> q.put("frist!")
    Gotit got data: frist!


.. _Zookeeper: http://zookeeper.apache.org/

.. image:: https://secure.travis-ci.org/davidmiller/zoop.png?branch=master
   :alt: Build Status
   :target: https://secure.travis-ci.org/davidmiller/zoop

Usage
=====

