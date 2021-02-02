"""
    First of the two converters used

    Performs dimensionality reduction by grouping together feilds in the data
    and converts it to JSON from CSV for easier training of our models
"""

# Import packages for cvs and json
import csv
import json

# Set the field names that we need
fieldNames = ("Target",)

# JSONify first weather station data as testing data
infile = open('../Data Dumps/Cleaned Data/weather_test.csv', 'r')
reader = csv.DictReader(infile, fieldNames, "Data")
with open('../Data JSON/weather_test.json', 'w+') as outfile:
    for row in reader:
        json.dump(row, outfile)
        outfile.write(",\n")    # JSON magic for less future hassle

# JSONify second weather station as training data
infile2 = open('../Data Dumps/Cleaned Data/weather_train.csv', 'r')
reader = csv.DictReader(infile2, fieldNames, "Data")
with open('../Data JSON/weather_train.json', 'w+') as outfile2:
    for row in reader:
        json.dump(row, outfile2)
        outfile2.write(",\n")   # More JSON magic
