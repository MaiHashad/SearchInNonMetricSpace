import csv
import pandas as pd
#df = pd.read_excel("nm_search_rank_matrix.xlsx")
#df.columns = df.columns.str.strip()
import ast
rank_matrix = []
rank_array = []
for i in range(0,2):
    rank_array = []
    file_name = (str(i) + ".csv")
    print(file_name)
    with open(file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
        
            #print(row)
            rank_array.append([int(x) for x in row])
            print(rank_array)
        rank_matrix.append(rank_array)
        
print(rank_matrix)