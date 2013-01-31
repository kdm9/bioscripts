#!/bin/bash
for i in *.sam
do
    awk '{OFS="\t"; print ">"$1"\n"$10}' <$i >`basename $i .sam`.fasta &
done

