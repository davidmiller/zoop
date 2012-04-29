"""
Fab commands for ZOOP
"""

from fabric.api import task, hosts, local, lcd,  cd, run
from fabric import operations

deadpan = "happenup@deadpansincerity.com"

@task
def make_docs():
    """
    Rebuild the documentation
    """
    with lcd("doc/"):
        local("make html")

@task
@hosts(deadpan)
def upload_docs():
    """
    Build, compress, upload and extract the latest docs
    """
    with lcd("doc/build/html"):
        local("rm -rf zoopdocs.tar.gz")
        local("tar zcvf zoopdocs.tar.gz *")
        operations.put("zoopdocs.tar.gz", "/home/happenup/webapps/zoopdocs/zoopdocs.tar.gz")
    with cd("/home/happenup/webapps/zoopdocs/"):
        run("tar zxvf zoopdocs.tar.gz")
