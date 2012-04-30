"""
zoop.logutils

ZooKeepr has the irritating quality of printin it's logs to sterr

Sometimes (mostly) this is not really a desirable thing
"""
import zookeeper

def divert_zoolog(logfile='/dev/null'):
    """
    Divert the ZooKeeper logging away from stderr.

    This is particularly useful in interactive sessions where
    the default logging behaviour is distinctly disruptive, but
    also useful when logging that output to a file is desired.


    Arguments:
    - `logfile`: string - path to the file we'll log to

    Return: None
    Exceptions: None
    """
    fh = open(logfile, 'w')
    zookeeper.set_log_stream(fh)
    return

def set_loglevel(level):
    """
    Set the ZooKeeper log level.

    Valid arguments are DEBUG|ERROR|INFO|WARN


    Arguments:
    - `level`: string

    Return: None
    Exceptions: None
    """
    zlevel = getattr(zookeeper, 'LOG_LEVEL_{0}'.format(level))
    zookeeper.set_debug_level(zlevel)
    return
