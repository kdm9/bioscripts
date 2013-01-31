#!/usr/bin/env python

import csv
import argparse
import os.path
from random import shuffle
from copy import deepcopy

def get_args():
    parser = argparse.ArgumentParser(description="Create a Completly"
            "Randomised Design experimental layout from a CSV file")
    parser.add_argument("-i", "--input", action="store", dest="input")
    parser.add_argument("-o", "--output", action="store", required=True,
            dest="output")
    parser.add_argument("-t", "--tray-dimensions", action="store",
            required=True, dest="tray")
    parser.add_argument("-r", "--replicates", action="store", default=1,
            required=True, dest="reps", type=int)
    parser.add_argument("-c", "--create", action="store_true", default=False,
            dest="create")
    return parser.parse_args()

def create_csv():
    """Writes a pro-forma csv to be filled in for input"""
    args = get_args()
    out_fh = open(args.output, "wt")
    out_fh.write('"Condition","Plant"')
    out_fh.close()

def get_tray_positions(tray_x, tray_y):
    positions = []
    for yyy in xrange(tray_y):
        y_str = ""
        # This generates the y-string backwards (from right to left)
        while yyy > 25:
            lhs = yyy // 26
            rhs = yyy % (lhs * 26)
            y_str = chr(rhs + 65) + y_str
            yyy = lhs - 1  # We expect yyy to be 0-indexed, lhs is 1-indexed
        y_str = chr(yyy + 65) + y_str
        for xxx in xrange(tray_x):
            positions.append(y_str + str(xxx+1))  # xxx 0-index, want 1-index
    return positions


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
    out_file = open(args.output, "wt")
    out_cols = ["Condition", "Tray", "Position", "Plant"]
    #out_cols = ["Condition", "Tray", "Position", "Replicate", "Plant"]
    out_csv = csv.DictWriter(out_file, out_cols)
    out_csv.writeheader()

    plant_dict = {}
    tray_dim = [int(s) for s in args.tray.split("x")]
    tray_pos = get_tray_positions(*tray_dim)
    tray_size = len(tray_pos)


    for line in in_csv:
        if line["Condition"] not in plant_dict:
            plant_dict[line["Condition"]] = []
        plant_dict[line["Condition"]].append(line["Plant"])

    tray_count = 0
    for condition, plants in plant_dict.iteritems():
        if args.reps > 1:
            these_plants = []
            for rrr in xrange(args.reps):
                for plant in plants:
                    these_plants.append("%s R%i" %(plant, rrr + 1))
        else:
            these_plants = plants
        tray_count += 1
        this_tray_pos = deepcopy(tray_pos)
        plant_count = 0
        for iii in xrange(1000):
            shuffle(these_plants)
        for plant in these_plants:
            if plant_count > tray_size:
                this_tray_pos = deepcopy(tray_pos)
                tray_count += 1
                plant_count = 0
            plant_count += 1
            row = {
                    "Condition": condition,
                    "Tray": tray_count,
                    "Position": this_tray_pos.pop(0),
#                    "Replicate": rrr + 1,
                    "Plant": plant
                    }
            out_csv.writerow(row)
    out_file.close()
    in_file.close()


if __name__ == "__main__":
    main()
