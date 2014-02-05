#!/bin/bash

echo -e "Sample\tUnique\tShared"
for p in 1 2 3 4 6
do
	for row in {A..H}
       	do
		for col in `seq 1 12`
		do
			stat_f=*plate${p}_${row}${col}_*.stats
			if [ -f $stat_f ]
			then
				echo $stat_f >&2
				unique=$(grep 'Total K-mers only found in' -A 3 $stat_f  |grep 'Hash 2' |cut -d ' ' -f 5 | tr -d '\n')
				shared=$(grep 'Total shared found in hash 2' $stat_f |cut -d ' ' -f 9 | tr -d '\n')
				echo -e "$p$row$col\t$unique\t$shared"
			fi
		done
	done
done
