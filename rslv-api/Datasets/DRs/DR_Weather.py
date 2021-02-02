import pandas as pd
import csv

# First Remove Unnecessary features
infile = pd.read_csv('../Data Dumps/Weather/{}_weather.csv'.format("IBELFAST4"), index_col='TemperatureC')

req_cols = ['DewpointC', 'Humidity', 'HourlyPrecipMM']

new_file = infile[req_cols]
new_file.to_csv("../Data Dumps/Cleaned Data/weather_clean.csv")

# Second Remove the column names coz SVM don't like em
with open('../Data Dumps/Cleaned Data/weather_clean.csv', 'r') as inp, open('../Data Dumps/Cleaned Data/weather_reduced.csv', 'w', newline='') as out:
    writer = csv.writer(out)

    for row in csv.reader(inp):
        if row[0] != 'TemperatureC':
            writer.writerow(row)

# EOF