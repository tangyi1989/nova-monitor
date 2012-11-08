local method   = ngx.var.request_method

if method != 'GET' then
	proxy_pass http://mycgiserver
else
	proxy_pass http://myhttpserver
