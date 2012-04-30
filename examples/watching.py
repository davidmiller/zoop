"""
Let's watch a node for children gettinig created
"""
import time

import zoop

from zoop import logutils, watch
logutils.set_loglevel('ERROR')

zk = zoop.ZooKeeper('localhost:2181')

def lprint(what):
    with watch.PLock:
        print what

def watchit(path, event):
    lprint("Watch it!")
    lprint(path)
    lprint(event)

zk.connect()

if zk.exists('/testme'):
    zk.delete('/testme')
if zk.exists('/festme'):
    zk.delete('/festme')

lprint("Registering watch")
zk.watch('/', watchit, zoop.Event.Child)
time.sleep(0.4)

print "Creating Node"
zk.create('/testme')

print zk.ls('/')
time.sleep(1)
zk.create('/festme')
time.sleep(1)
