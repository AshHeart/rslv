import csv
import time
import dill as pickle

pass_list = []

with open('./Datasets/Data Dumps/Cleaned Data/friction_reduced.csv', 'r') as friction:
    reader = csv.reader(friction)
    
    for row in reader:
        for i in row:
            pass_list.append(i)
                
            with open('./API/fric_value.pk', 'wb') as f:
                pickle.dump(pass_list, f)

            time.sleep(300)
            pass_list = []
            break