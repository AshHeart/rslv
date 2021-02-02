import csv
import time
import dill as pickle

pass_list = []

with open('./Datasets/Data Dumps/Cleaned Data/weather_reduced.csv', 'r') as weather:
        reader = csv.reader(weather)

        for row in reader:
            for i in row:
                pass_list.append(i)
                
                with open('./API/pred_results.pk', 'wb') as f:
                    pickle.dump(pass_list, f)

                time.sleep(300)
                pass_list = []
                break  
    
