#!/bin/bash

for i in 0{1..2}
do
  echo Problem $i:
  python3 gsm_network.py < tests/$i.txt
  echo
done
