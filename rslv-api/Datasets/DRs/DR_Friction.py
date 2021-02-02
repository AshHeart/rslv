import pandas as pd
import csv

# First separate only the frcition value for live data
infile=pd.read_csv('../Data Dumps/Data Split 2/friction_train.csv')

keep_col = ['Friction']

new_file = infile[keep_col]
new_file.to_csv('../Data Dumps/Cleaned Data/friction_cleaned.csv', index=False)

# Now remove the darm header row
with open('../Data Dumps/Cleaned Data/friction_cleaned.csv', 'r') as inp, open('../Data Dumps/Cleaned Data/friction_reduced.csv', 'w', newline='') as out:
    writer = csv.writer(out)

    for row in csv.reader(inp):
        if row[0] != 'Friction':
            writer.writerow(row)

# EOF