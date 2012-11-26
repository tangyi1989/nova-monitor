import json
import urllib2
import time

data0={
    'cmd': 'heart_info', 
    'data': 'tmd', 
    'data2': {
        'mem': 12.3, 
        'cpu': 'ttmd'
    }
}
url='http://127.0.0.1:7103'

data=json.dumps(data0)
print 'data:',data,',type:',type(data)

req=urllib2.Request(url,data,{'Content-Type': 'application/json'})
f=urllib2.urlopen(req)

print f.read()

