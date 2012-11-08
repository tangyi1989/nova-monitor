#!/usr/bin/python

import eventlet
from eventlet.green import socket

PORT=6000
BACKLOG=2

def Svr_Handle(client):
    client.send("Hello!I'm a server made by eventlet...")
    while True:
        c = client.recv(1000)
        if not c: break
        print "Recv From %s:%s" %(client,c)
        #client.send(c)
    client.close()
    print "Something is wrong with %s..." %client

server = eventlet.listen(('0.0.0.0', PORT))
pool = eventlet.GreenPool(50)
print "ChatServer starting up on port %s" % PORT

while True:
    print "Waiting for a client..."
    new_sock, address = server.accept()
    print "A client joined..."
    
    pool.spawn_n(Svr_Handle, new_sock)

print "OK?"

