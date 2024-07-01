

# Print out zero to 200 

source_folder1=${1}
source_folder2=${2}

file_name_template="run0000_genGEN_obj.csv"

for i in {1..200}
do

  # pad i with four zeros
  gen_num=$(printf "%04d" $i)
  

  file_name=$(echo $file_name_template | sed "s/GEN/${gen_num}/g")

  python utilities/comparePlots.py ${i} NSGA-II PI-NSGA-II ${source_folder1}/${file_name} ${source_folder2}/${file_name}

done




