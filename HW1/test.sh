#!/usr/bin/env bash 
counter=0

for i in {1..50}
do 
	echo "Running: $i"
	RES=$(./homework.py --input testcases/input$i.txt --answers testcases/output$i.txt)
	if [[ $RES == "True" ]]; then
		counter=$(($counter+1))
	else
		echo "$RES"
	fi

done
echo $counter
echo "All done!!"