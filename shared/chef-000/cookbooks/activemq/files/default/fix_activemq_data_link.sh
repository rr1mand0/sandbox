#!/bin/sh
BASE_DIR=/usr/local/lib/activemq
DATA_DIR=/var/activemq
if [ `readlink $BASE_DIR/data` = "/usr/local/activemq" ] 
then 
	rm $BASE_DIR/data 
	ln -s $DATA_DIR $BASE_DIR/data
fi 
