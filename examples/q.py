import time
import zoop

zoop.divert_zoolog()

zk =  zoop.ZooKeeper('localhost:2181')

zk.connect()

q = zoop.Queue(zk, '/testme')

def gotit(data):
    print "Gotit got data", data

q.flush()

q.watchitem(gotit)

q.put("frist!")
time.sleep(1)
q.put("Next!")
time.sleep(1)
