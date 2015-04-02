#!/usr/bin/env python
from __future__ import print_function

from sys import version_info
if version_info[0] == 3:  # py3k compatibility
    xrange = range

import csv
import argparse
import os.path
from random import shuffle
from copy import deepcopy


def get_args():
    """Get program command line arguments"""
    parser = argparse.ArgumentParser(description="Create a Completly"
            "Randomised Design experimental layout from a CSV file")
    parser.add_argument("-i", "--input", action="store", dest="input",
            help="Input file path, must exist")
    parser.add_argument("-o", "--output", action="store", required=True,
            dest="output", help="Output file path.")
    parser.add_argument("-t", "--tray-dimensions", action="store",
            required=True, dest="tray", help="The dimensions of the tray,"
            " given as <rows>x<cols> (note that's a lower case letter x)")
    parser.add_argument("-R", "--replicates-together", action="store_true",
            default=False, dest="reps_together", help="Should all plants in a"
            " replicate block be grouped together?")
    parser.add_argument("-r", "--replicates", action="store", default=1,
            required=True, dest="reps", type=int, help="The number of"
            " replicates per plant and condition")
    parser.add_argument("-c", "--create", action="store_true", default=False,
            dest="create", help="Flag, creates a pro-forma CSV to enter"
            " conditions and plants into")
    return parser.parse_args()


def create_csv():
    """Writes a pro-forma csv to be filled in for input"""
    args = get_args()
    out_fh = open(args.output, "wt")
    out_fh.write('"Condition","Plant"')
    out_fh.close()


def get_tray_positions(tray_x, tray_y):
    """Gets a list of tray positions from some dimensions.
    >>> get_tray_positions(2,3)
    ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    """
    positions = []
    for yyy in xrange(tray_y):
        y_str = ""
        # This generates the y-string backwards (from right to left), hence
        # y_str = str + y_str, not just y_str += str
        while yyy >= 26:  # Note the >=
            lhs = yyy // 26  # the most signficant character(s)
            rhs = yyy % (lhs * 26)  # the least significant (single) char
            y_str = chr(rhs + 65) + y_str
            yyy = lhs - 1  # We expect yyy to be 0-indexed, lhs is 1-indexed
        y_str = chr(yyy + 65) + y_str
        for xxx in xrange(tray_x):
            positions.append(y_str + str(xxx + 1))  # xxx 0index, want 1index
    return positions


def main():
    """Main program logic"""
    args = get_args()

    # Create experiment proforma and exit, if requested
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
    total_plant_count = 0
    condition_count = 0

    # For each condition, create tray(s) of it's plants
    for condition, plants in plant_dict.items():
        condition_count += 1

        # Get a list of all the plants for this condition
        if args.reps > 1:
            if args.reps_together:
                pass
            else:
                these_plants = []
                for rrr in xrange(args.reps):
                    for plant in plants:
                        these_plants.append("%s R%i" % (plant, rrr + 1))
        else:
            these_plants = plants

        tray_count += 1
        # Must deepcopy, otherwise we remove positions when we pop(0) below
        this_tray_pos = deepcopy(tray_pos)
        plant_count = 0

        # Randomise order, 1000 shuffles is really quick and should be random
        # enough
        for iii in xrange(1000):
            shuffle(these_plants)

        for plant in these_plants:
            total_plant_count += 1
            plant_count += 1

            # Create new tray if the current one is full
            if plant_count >= tray_size:
                # Must deepcopy, see above
                this_tray_pos = deepcopy(tray_pos)
                tray_count += 1
                plant_count = 0

            # Form and write the row
            row = {
                    "Condition": condition,
                    "Tray": tray_count,
                    "Position": this_tray_pos.pop(0),
                    "Plant": plant
                    }
            out_csv.writerow(row)
    out_file.close()
    in_file.close()

    # Print a summary
    print("Done!")
    print("Processed %i replicates of %i experimental conditions" %
            (args.reps, condition_count))
    print("Which gives a total of %i plants" % total_plant_count)


if __name__ == "__main__":
    main()
