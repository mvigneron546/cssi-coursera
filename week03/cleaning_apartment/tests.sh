#!/bin/bash

for i in 0{1..2}
do
  echo Problem $i:
  python3 cleaning_apartment.py < tests/$i.txt
  echo
done
