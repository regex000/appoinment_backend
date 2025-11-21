"""Gunicorn configuration file for Render deployment with ASGI support"""

import os
import multiprocessing

# Server socket - bind to the PORT environment variable or default to 8000
port = os.getenv('PORT', '8000')
bind = f"0.0.0.0:{port}"
backlog = 2048

# Worker processes - use uvicorn workers for ASGI support
workers = int(os.getenv('WORKERS', max(2, multiprocessing.cpu_count())))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "modern-hospital-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
ssl_version = None
cert_reqs = 0
ca_certs = None
suppress_ragged_eof = True
do_handshake_on_connect = False
ciphers = None

# Application
raw_env = []

# Preload app to catch startup errors early
preload_app = False

# Worker class settings for uvicorn
worker_class_str = "uvicorn.workers.UvicornWorker"
