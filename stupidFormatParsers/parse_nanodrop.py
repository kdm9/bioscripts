from __future__ import print_function
import csv
from docopt import docopt

__doc__ = """
Usage:
    parse_nanodrop.py <input> <output> [--keys=KEYS]

Options
    --keys=KEYS   Keys to keep. Comma seperated list. By default:
                      Sample ID
                      ng/ul
                      260/280
                      260/230
"""


def main():
    opts = docopt(__doc__)
    print(opts)
    infn = opts["<input>"]
    outfn = opts["<output>"]

    if opts["--keys"]:
        keys_to_keep = opts["--keys"].strip().split(",")
    else:
        keys_to_keep = ["Sample ID", "ng/ul", "260/280", "260/230"]

    with open(infn) as infh:
        reader = csv.DictReader(infh, dialect="excel-tab")
        samples = list(reader)

    output_samples = []
    for sample in samples:
        print(sample.keys())
        sample = {k.strip(): v.strip() for k, v in sample.iteritems()}
        out_sample = {k: sample[k] for k in keys_to_keep}
        print(out_sample)
        output_samples.append(out_sample)

    with open(outfn, "w") as outfh:
        writer = csv.DictWriter(outfh, keys_to_keep)
        writer.writeheader()
        for sample in output_samples:
            writer.writerow(sample)


if __name__ == "__main__":
    main()

