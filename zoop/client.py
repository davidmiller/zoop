"""
zoop.client
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


class ZooKeeper(object):
    """
    The ZooKeeper client

    Arguments:
    - `connection`: string of host:port
    """

    def __init__(self, connection):
        """
        Create the zookeeper.client instance

        Arguments:
        - `connection`: string host:port
        """
        self.server = connection
        self._zk = None
        return

    def connect(self):
        """
        Create a connection to the ZooKeeper instance

        Return: None
        Exceptions: None
        """
        self._zk = zookeeper.init(self.server, self._eventhandler)

    def _eventhandler(self, zk, etype, conn, path):
        """
        Callback for libzookeeper that fires when ZooKeeper events occur.

        Dispatch to our own callbacks.

        Arguments:
        - `zk`: handle to the ZooKeeper connection
        - `etype`: Enum- Event type
        - `conn`: Enum Connection Status
        - `path`: string- Path that the event occured

        Return: None
        Exceptions: None
        """
        pass





