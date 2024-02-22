#!/bin/bash

IFS='\n'

year=${1}
file=${2}


if [[ $(($year % 4)) -eq 0 ]]; then 
  plant_date=136
else
  plant_date=135
fi

short_year="${year:2:3}"


while read p; do
  echo "$p" | sed -e "s/ZZ/${short_year}/g" -e "s/QQQ/${plant_date}/g"
done < $file



