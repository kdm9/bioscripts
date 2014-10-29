import csv
import sys
rows = list(csv.reader(sys.stdin))
writer = csv.writer(sys.stdout)
for col in range(len(rows[0])):
        writer.writerow([row[col] for row in rows])
