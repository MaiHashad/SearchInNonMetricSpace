import csv
import os

comp_count = 0
data_file_names = os.listdir("out")
for data_file in data_file_names:
    data = list(csv.reader(open("out/{}".format(data_file), "r")))
    for row in data:
        comp_count += len(row)

print("{} total comparisons".format(comp_count))