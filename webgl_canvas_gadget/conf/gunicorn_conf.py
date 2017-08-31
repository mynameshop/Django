from __future__ import unicode_literals
import os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SITE_ROOT_DIR_PATH = os.path.join(CURRENT_DIR, '..', '..')
SITE_LOGS_DIR_PATH = os.path.join(SITE_ROOT_DIR_PATH, '.logs')
SITE_PIDS_DIR_PATH = os.path.join(SITE_ROOT_DIR_PATH, '.pids')
SITE_SOCKETS_DIR_PATH = os.path.join(SITE_ROOT_DIR_PATH, '.sockets')

proc_name = os.path.basename(CURRENT_DIR)

bind = 'unix:' + os.path.join(SITE_SOCKETS_DIR_PATH, 'gunicorn.socket')

workers = os.cpu_count() #* 2 + 1
threads = 1

max_requests = 256
max_requests_jitter = 128

accesslog = os.path.join(SITE_LOGS_DIR_PATH, 'gunicorn-access.log')
errorlog = os.path.join(SITE_LOGS_DIR_PATH, 'gunicorn-error.log')