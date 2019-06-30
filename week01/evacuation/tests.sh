#!/bin/bash

for i in 0{1..9} {10..36}
do
  echo Problem $i:
  output=$(python3 evacuation.py < tests/$i)
  answer=$(cat tests/$i.a)
  if [ "$output" == "$answer" ]
  then
    echo Correct Answer!
  else
    echo Incorrect Answer!
    echo Program Output: $output
    echo Answer: $answer
    break
  fi
  echo
done
