#!/bin/bash
for i in * ; do
	if [ -f $i ]; then
    cat "$i" |while read line; do 
        if [ "${line:0:1}" == ">" ]; then
        	species="$(echo $i | cut -d " " -f 1 | head -c 10)-$(echo $i | cut -d "-" -f 2- | sed 's/ /-/g' | tail --bytes=19)"
		#species="$(echo $i| cut -d " " -f 1 | head -c 10)-$(echo $i| cut -d " " -f 2- | sed 's/ /-/g'| tail -c 10)-$(cat "$i"| grep -v ">" |sed ':a;N;$!ba;s/\n//g'| wc -c)"
        	#species="$(echo $i |sed 's/>//g' )"
        	#(echo $line |cut -d "[" -f 2 | cut -d ":" -f 1)
        	echo  ">$species"
        	
	    else
		    echo $line
	    fi
    done 
	fi
done;
