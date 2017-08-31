from __future__ import absolute_import

import dj_database_url

from .base import *

DEBUG = False
SITE_ID = 4
DATABASE_URL = "postgres://uwrdljmjulfmbj:e5Ru0MfLmm3zRc7Ze4Um7Du6SB@ec2-23-21-42-29.compute-1.amazonaws.com:5432/danivfm2pe2i1v"
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL,
                                              conn_max_age=500)


ROLLBAR = {
    'access_token': '174e388b95d54725822b0997121c70ce',
    'environment': 'staging',
    'branch': 'master',
    'root': os.getcwd(),
}
