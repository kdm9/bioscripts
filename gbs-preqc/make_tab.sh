#!/bin/bash

echo -e "Sample\tRef\tUnique\tShared"
for ref in "2_C5" "6_D6" "6_D5" "6_D8" "6_D7"
do
	for p in 1 2 3 4 6
	do
		for row in {A..H}
		do
			for col in `seq 1 12`
			do
				stat_f=kat*plate${p}_${row}${col}_*ref_plate$ref*.stats
				echo $stat_f >&2
				if [ -f $stat_f ]
				then
					unique=$(grep 'Total K-mers only found in' -A 3 $stat_f  |grep 'Hash 2' |cut -d ' ' -f 5 | tr -d '\n')
					shared=$(grep 'Total shared found in hash 2' $stat_f |cut -d ' ' -f 9 | tr -d '\n')
					echo -e "$p$row$col\t$ref\t$unique\t$shared"
				fi
			done
		done
	done
done
