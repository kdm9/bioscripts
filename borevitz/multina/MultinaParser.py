#!/usr/bin/python
import csv
import sys
import re
infile = "/home/kevin/multina.csv"
outfile = "/home/kevin/multina.out.csv"
parser = csv.reader(open(infile, "rb"))
write = csv.writer(open(outfile, "wb"))
well_regex = re.compile(r"\)(\S+)\:")
header = 0
well_list = []
write.writerow(["Index","Well","Size","Intensity"]) #this is the header
for row in parser:
    if header == 0:
        #create the well list, such that the well name can be used.
        for i in range(1,len(row), 2):
            well_search = well_regex.search(row[i])
            well_list.append(well_search.group(1))
        header = 1
        continue
    index = row[0]
    for i in range(1,len(row), 2):
        this_record = []
        #"Index","Well","Size","Intensity"
        size = row[i]
        well_index= (i-1)/2 #allows integration with the well list above
        intensity = row[i+1]
        this_record.append(index)
        this_record.append(well_list[well_index])
        this_record.append(size)
        this_record.append(intensity)
        write.writerow(this_record)

