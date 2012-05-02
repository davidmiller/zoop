import threading
import time

import zoop

zoop.divert_zoolog()

zk =  zoop.ZooKeeper('localhost:2181')
zk.connect()

if zk.exists('/zooplocks/mylock'):
    zk.delete('/zooplocks/mylock')

def t1():
    lk = zoop.Lock(zk, 'mylock')
    with lk:
        time.sleep(1)
        print "Thread one", zk.get_children('/zooplocks/mylock')
        time.sleep(1)

def t2():
    lk = zoop.Lock(zk, 'mylock')
    with lk:
        print "Thread two", zk.get_children('/zooplocks/mylock')
        time.sleep(0.1)

threads = [
    threading.Thread(target=t1),
    threading.Thread(target=t2)
    ]

for t in threads:
    t.start()

for t in threads:
    t.join()


print zk.get_children('/zooplocks/mylock')
