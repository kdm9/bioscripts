#!/bin/bash

for file in *.JPG
do
    exifcmd="exiftool -a -gps:all"
    cutcmd=""
    lat=$($exifcmd "$file" 2>/dev/null | grep Latitude | cut -d : -f 2 | tr -d '\n' | sed -e 's/\s+//g')
    long=$($exifcmd "$file" 2>/dev/null | grep Longitude | cut -d : -f 2 | tr -d '\n' | sed -e 's/\s+//g')
    alt=$($exifcmd "$file" 2>/dev/null | grep Altitude | cut -d : -f 2 | tr -d '\n' | sed -e 's/\s+//g')
    echo "$file,$lat,$long,$alt"
done
