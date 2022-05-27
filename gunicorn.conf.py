workers = 2
bind = '0.0.0.0:8000'
backlog = 2048

errorlog = 'error.log'
loglevel = 'info'
accesslog = 'access.log'
capture_output = True
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'