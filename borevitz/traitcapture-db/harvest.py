from __future__ import print_function
from csv import DictReader, DictWriter
from docopt import docopt
from datetime import datetime as dt

__doc__ = """
USAGE:
    harvest.py -p PLANT_DB -s SAMPLE_DB -o OUT_CSV

OPTIONS:
    -s SAMPLE_DB    Sample DB CSV file. Headers should include:
                        ID,PlantName,Accession,Chamber,TrayPos
    -p PLANT_DB     Plant DB CSV file. Headers should include:
                        ID,PlantID
    -o OUT_CSV      Output CSV file

enter a - on a line
"""

def _make_db_dict(filename):
    ifh = open(filename)
    reader = DictReader(ifh)
    db_dict = {}
    for record in reader:
        db_dict[record["ID"]] = record
    ifh.close()
    return db_dict


def main():
    opts = docopt(__doc__)

    plant_dict = _make_db_dict(opts["-p"])
    print("Read Plant DB: Found %i plants" % len(plant_dict))

    sample_dict = _make_db_dict(opts["-s"])
    print("Read Sample DB: Found %i samples" % len(sample_dict))

    ofh = open(opts["-o"], "w")
    out_header = ["SampleID","PlantID","CollectionTime"]
    writer = DictWriter(ofh, out_header)
    writer.writeheader()

    exit = False
    while not exit:
        try:
            # wait for plant scan
            print("Scan plant barcode")
            plant_id = raw_input("Pot >")

            try:
                plant = plant_dict["plant_id"]
            except KeyError:
                print("ERROR: plant id '%s' not in database" % plant_id)
                continue
            print("Plant is '%s' from %s position %s" % (
                    plant["PlantName"],
                    plant["ExperimentGrowthLocation"],
                    plant["TrayPosition"])
                    )

            print("Scan sample barcode")
            # wait for tube scan
            sample_id = raw_input("Pot >") 
            try:
                sample = sample_dict[sample_id]
            except KeyError:
                print("ERROR: sample id '%s' not in database" % sample_id)
                continue

            if sample["PlantID"] == plant_id:
                print("match")
            else:
                print("MISMATCH!!!!!")
                print("Should we write anyway? y/[n]")
                if not "y" in raw_input():
                    continue
            writer.writerow({
                "SampleID": sample_id,
                "PlantID": plant_id,
                "CollectionTime": dt.strftime(dt.now(), "%y-%m-%dT%H:%M:%S")
                })
        except KeyboardInterrupt:
            exit = True
            ofh.close()

if __name__ == "__main__":
    main()
