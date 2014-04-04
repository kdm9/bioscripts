import csv
import copy
import json

def main(infn, outfn):
    ifh = open(infn)
    rdr = csv.DictReader(ifh)
    dct = {}
    for line in rdr:
        dct[line["ID"]] = copy.deepcopy(line)
    ofh = open(outfn, "w")
    json.dump(dct, ofh)
    ofh.close()
    ifh.close()

if __name__ == "__main__":
    from sys import argv
    main(argv[1], argv[2])
