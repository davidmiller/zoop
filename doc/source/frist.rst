.. _frist:

===========
First Steps
===========

So, you're all installed and ready to go...

Making A Connection
===================

The first thing you'll need is to create a client that's connected to your ZooKeeper instance::

    >>> import zoop
    >>> zoop.divert_zoolog()
    >>> zk = zoop.ZooKeeper('localhost:2181')
    >>> zk.connect()
    >>> print zk
    <ZooKeeper Client for localhost:2181>

1. Most things you'll need to do are accessible from the main zoop namespace.
2. By default libzookeeper prints a *lot* of DEBUG trace to stderr. This is quite unpleasant, so let's stop that.
3. The single argument here is the host:port of the ZooKeeper instance you're connecting to.
4. We have to create the connection explicitly.

CR(eate) U(pdate) D(estroy)
===========================

Now that we have a connection, we can start to do something useful with it::

    >>> zk.get_children('/')
    ['zookeeper']
    >>> zk.create('/frist')
    '/frist'
    >>> zk.create('/frist/hello', 'Hello Beautiful World')
    '/frist/hello'

1. Keeping up the Filesystem metaphor, this is essentially *nix *ls*.
2. Creating a Node requires an absolute path.
3. The optional second argument is the Value of the Node.


So - let's start accessing our creations::

    >>> zk.get('/frist/hello')
    ('Hello Beautiful World', {'pzxid': 737L, 'ctime': 1336029934025L, 'aversion': 0, 'mzxid': 737L, 'numChildren': 0,
 'ephemeralOwner': 0L, 'version': 0, 'dataLength': 21, 'mtime': 1336029934025L, 'cversion': 0, 'czxid': 737L})
    >>> zk.set('/frist/hello', 'Hello Again')
    >>> zk.get('/frist/hello')[0]
    'Hello Again'

1. The get() method returns a tuple of (Value dictionary-of-stats)
2. We can update an existing Node

And when we're done::

    >>> zk.delete('/frist/hello')
    >>> zk.get_children('/')
    ['zookeeper']

1. Deleting nodes uses the succinctly-named delete() method.

Watching for changes
====================

One of the fundamental principles of ZooKeeper is the registering of
callbacks when changes occur elsewhere in your system.

With zoop we do this by registering a watch function::

    >>> def watchit(path, event):
    ...     print "Watching it!", path, zoop.Event.human(event)
    ...
    >>> zk.watch('/frist/hello/', watchit, zoop.Event.Changed)
    >>> zk.set('/frist/hello', 'Oh what a beautiful morning!')
    Watching it! /frist/hello, Changed

You can watch for Change, Deleted, or Child events on a Node.