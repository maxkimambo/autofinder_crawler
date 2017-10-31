from queue import MessageQueue
import json

myqueue = MessageQueue()

for x in range(100):
    myqueue.publish({x:x})
