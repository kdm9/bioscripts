#!/usr/bin/env python

import csv
import argparse
import os.path

def get_args():
    parser = argparse.ArgumentParser(description="Create a Completly"
            "Randomised Design experimental layout from a CSV file")
    parser.add_argument("-i", "--input", action="store", dest="input")
    parser.add_argument("-o", "--output", action="store", required=True,
            dest="output")
    parser.add_argument("-t", "--tray-dimensions", action="store",
            required=True, dest="tray")
    parser.add_argument("-c", "--create", action="store_true", default=False,
            dest="create")


    return parser.parse_args()

def create_csv():
    """Writes a pro-forma csv to be filled in for input"""
    args = get_args()
    out_fh = open(args.output, "wt")
    out_fh.write('"Condition","Plant"')
    out_fh.close()


def main():
    args = get_args()

    if args.create:
        create_csv()
        exit()
    
    # Check input file exist
    if not os.path.isfile(args.input):
        ValueError("Input file must exist: %s" % args.input)
        
    in_file = open(args.input, "rt")
    in_csv = csv.DictReader(in_file)

    plant_dict = {}

    for line in in_csv:
        if line["Condition"] not in plant_dict:
            plant_dict[line["Condition"]] = []
        plant_dict[line["Condition"]].append(line["Plant"])

    import json
    print json.dumps(plant_dict, sort_keys=True, indent=2)



if __name__ == "__main__":
    main()
