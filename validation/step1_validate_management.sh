#!/bin/zsh

# don't forget to conda activate! 

root_dir="$(dirname $0)"

cd $root_dir
cd ..

output_file="./dhome/Weather/CASSREPR.WTH"

i=0

for wfile in $(ls -1 ./dhome/Weather/*WTD) 
do

  echo "*WEATHER DATA : CAMI"                                    > ${output_file}
  echo ""                                                       >> ${output_file}
  echo "@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT" >> ${output_file}
  echo "  CAMI   41.931  -86.002   231   9.4  26.6 -99.0 -99.0" >> ${output_file}
  cat $wfile | sed 's/G/ /g'                                    >> ${output_file}


  python validation_step1_validate_management.py $i
  i=$(expr $i + 1)

  

done


