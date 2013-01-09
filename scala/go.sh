#!/bin/bash

scalac ParseProductDSL.scala
if [ $? = 0 ];
then
  echo "generating merge.txt"
  time scala ParseProductDSL products.txt listings.txt merge.txt
else
  echo "error compiling ParseProductDSL.scala"
fi

