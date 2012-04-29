"""
zoop._zookeeper

Because we want to run unittests on Travis-CI where installing the
libzookeeper bindings is non-trivial, let's wrap the import with a
Travis-CI mock.
"""
import os

try:
    import zookeeper
except ImportError:
    if os.environ.has_key('TRAVIS') and os.environ['TRAVIS'] == 'true':
        import mock
        zookeeper = mock.MagicMock(name='zookeeper')
    else:
        raise
