#!/bin/bash
filename=""
cat "$1" |while read line; do 
    if [ "${line:0:1}" == ">" ]; then
    	#species="$(echo $line |cut -d "[" -f 2 | cut -d ":" -f 1|sed 's/\//-/g'|sed 's/]//g')"
    	species="$(echo $line | sed 's/://g' |sed 's/>//g'|sed 's/\//-/g'|sed 's/]//g'|cut -d " " -f 1)"
	if [ -e "$species" ]; then
    		filename="$species.2"
	else
		filename="$species"
	fi
    	echo  "$line" >"$filename"
    else
    	echo  "$line" >> "$filename"
    fi
done 
