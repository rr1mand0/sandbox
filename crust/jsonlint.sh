#!/bin/bash

INFILE=$1
JSON_TMP=`mktemp /tmp/json.XXXXXX`

cat $INFILE |python -c "import sys, json; print json.dumps( json.load(sys.stdin), sort_keys=True, indent=2)" 2>/tmp/err.log >$JSON_TMP

rc=$?
echo rc=$?
if [[ $? == 0 ]];
then
  file=$JSON_TEMP 
else
  file=$INFILE
fi
cat $file
