#!/usr/bin/env python

import web
urls = ("/.*", "hello")
class hello: 
	def GET(self): 
		print "hhhhh"
		return 'Hello, world!' 
print "nani~~~~"
app = web.application(urls, globals()) 
application = app.wsgifunc() 
