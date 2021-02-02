'''
    Our second of two converters

    Converters are step two in dimentionality reduction after feature selection
    Here we convert the data from a .csv format to JSON for easy readability
    and eventual training of the friction model
'''

#We need both csv and json functionality
import csv
import json

#Field names for JSON data, for easy target and data splitting during training and evaluation
fieldNames = ("Target", )

#First convert the training data to json
with open('../Data Dumps/Data Split 2/friction_train.csv', 'r') as infile:
    reader = csv.DictReader(infile, fieldNames, "Data")
    with open('../Data JSON/friction_train.json', 'w+') as outfile:
        for row in reader:
            json.dump(row, outfile)
            outfile.write(",\n")    #JSON formatting magic for less hassle

#Now convert the testing data to json
with open('../Data Dumps/Data Split 2/friction_test.csv', 'r') as infile:
    reader = csv.DictReader(infile, fieldNames, "Data")
    with open('../Data JSON/friction_test.json', 'w+') as outfile:
        for row in reader:
            json.dump(row, outfile)
            outfile.write(",\n")    #Some more formatting magic

#END
