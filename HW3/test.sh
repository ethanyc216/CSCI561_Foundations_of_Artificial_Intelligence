#!/usr/bin/env bash 
counter=0

#for i in {1..50}
for i in {  24 25 }
do 
	echo "Running: $i"
	RES=$(./homework.py --input grade/input_$i.txt --answers grade/output_$i.txt)
	if [[ $RES == "True" ]]; then
		counter=$(($counter+1))
	else
		echo "$RES"
	fi

done
echo $counter
echo "All done!!"