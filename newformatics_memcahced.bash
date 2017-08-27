#!/bin/bash
NAME="newformatics_memcached"
SOCKETFILE="/home/misha/Desktop/webprojects/newformatics/newformatics_memcached.sock"
USER=misha
MEMORYUSAGE=128

#-d don't need this as will be used with supervisor
# ps -ef | grep supervisord
#sudo kill -s SIGTERM 1488
# sudo supervisord -c /etc/supervisor/supervisord.conf

exec memcached -m $MEMORYUSAGE -u $USER memory -s $SOCKETFILE