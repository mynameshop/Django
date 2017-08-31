#!/bin/bash

APP_NAME=$1

echo "Starting $APP_NAME"

cd `dirname $0`
SCRIPT_PATH=`pwd -P`
cd $SCRIPT_PATH
cd ../

RUNDIR=../.sockets/
test -d $RUNDIR || mkdir -p $RUNDIR

source ../.env/bin/activate
gunicorn wsgi:application -c ./conf/gunicorn_conf.py