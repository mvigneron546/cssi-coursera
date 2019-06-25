#!/bin/bash

for i in 0{1..9} {10..36}
do
  echo Problem $i:
  python3 evacuation.py < tests/$i
  cat tests/$i.a
done
