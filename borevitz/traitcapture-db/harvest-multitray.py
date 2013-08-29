from __future__ import print_function
from csv import DictReader, DictWriter
from docopt import docopt
from datetime import datetime as dt
from copy import deepcopy
import os

__doc__ = """
USAGE:
    harvest-multitray.py  -s SAMPLE_TYPES -d PLANT_DB -o OUT_DIR

OPTIONS:
    -s SAMPLE_TYPES Comma seperated list of sample types.
    -d PLANT_DB     Plant DB CSV file. Headers should include:
                        ID,PlantID
    -o OUT_DIR      Output CSV Directory.

Enter a - on a line to abort a scan
Just hit enter to not record a sample
"""

def _make_db_dict(filename):
    ifh = open(filename)
    reader = DictReader(ifh)
    db_dict = {}
    for record in reader:
        db_dict[str(record["ID"])] = record
    ifh.close()
    return db_dict

def main():
    opts = docopt(__doc__)

    plant_dict = _make_db_dict(opts["-d"])
    print("Read Plant DB: Found %i plants" % len(plant_dict))
    from json import dumps
    print(dumps(plant_dict, indent=2))


    sample_types = opts["-s"].strip().split(",")
    if len(sample_types) < 1:
        raise ValueError("Bad sample string '{}'".format(opts["-s"]))

    out_header = ["SampleID","PlantID","CollectionTime","PlateCoord"]
    out_files = {}
    file_d = {
            "name":"",
            "fh": None,
            "writer": None,
            "counter":0
            }

    for sample_type in sample_types:
        out_files[sample_type] = deepcopy(file_d)
        fn = os.path.join(opts["-o"], "%s.csv" % sample_type)
        out_files[sample_type]["name"] = fn
        out_files[sample_type]["fh"] = open(fn, "w")
        out_files[sample_type]["writer"] = DictWriter(
                out_files[sample_type]["fh"],
                out_header
                )
        out_files[sample_type]["writer"].writeheader()

    exit = False
    while not exit:
        try:
            write_d = {}
            # wait for plant scan
            print("Scan plant barcode")
            plant_id = "-"
            while "-" in plant_id:
                plant_id = raw_input("Pot >").strip()

            try:
                plant = plant_dict[plant_id]
            except KeyError:
                print("ERROR: plant id '%s' not in database" % plant_id)
                continue
            print("Plant is '%s' from %s position %s" % (
                    plant["PlantName"],
                    plant["ExperimentGrowthLocation"],
                    plant["TrayPosition"])
                    )

            for sample_type in sample_types:
                print("Scan sample barcode")
                sample_id = "-"
                while "-" in sample_id:
                    sample_id = raw_input("Tube (for %s) >" % sample_type).strip() 

                write_d[sample_type] = {
                    "SampleID": sample_id,
                    "PlantID": plant_id,
                    "CollectionTime": dt.strftime(dt.now(), "%y-%m-%dT%H:%M:%S")
                    }

            print("%s goes into tubes:" % plant["PlantName"])
            for sample_type in sample_types:
                print("%s: %s" %  (
                    sample_type,
                    write_d[sample_type]["SampleID"]
                    ))
            print("Should we write? [Y]/n")
            if not "n" in raw_input().lower():
                for sample_type in sample_types:
                    out_files[sample_type]["writer"].writerow(write_d[sample_type])


        except (KeyboardInterrupt, EOFError):
            exit = True

    print()
    for sample_type in sample_types:
        out_files[sample_type]["fh"].close()

if __name__ == "__main__":
    main()
