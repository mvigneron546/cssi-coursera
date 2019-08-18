#!/bin/bash

for i in 0{1..3}
do
  echo Problem $i:
  output=$(python3 plan_party.py < tests/$i)
  answer=$(cat tests/$i.a)
  if [ "$output" == "$answer" ]
  then
    echo Correct Answer!
  else
    echo Incorrect Answer!
    echo Program Output: $output
    echo Answer: $answer
  fi
  echo
done
