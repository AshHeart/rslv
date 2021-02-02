"""
    Our first of three models

    This one takes weather data and determines slippage based on rainfall
    Assginst a confidence value of 0-1, 0 being least and 1 being most likely to cause slippage

    Classifier used: K-sample Support Vector Machine
    Training Data: Weather data pulled from the file "rslv/Datasets/Data JSON/weather_train.json"
    Testing Data: Weather data pulled from the file "rslv/Datasets/Data JSON/weather_test.json"

    Samples Used:
        Training: 300
        Testing: 50

    TODO: "Modify for deployment"
"""

# Import our Classifier ie, Support Vector Machine from Scikit-Learn's built-in library
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# For deploying our trained model
import dill as pickle

# For some data wrangling
import json

# Ready our variables
data_train = []
label_train = []

# Ready more of our variables
data_test = []
label_test = []

# Get and format training data
with open("../Datasets/Data JSON/weather_train.json", "r") as train_in:
    data = json.load(train_in)

    for obj in data["train"]:
        data_train.append(obj["Data"])
        label_train.append(float(obj["Target"]))

print("Training data is\n")
print(data_train)
print(label_train)

# Get and format testing data
with open("../Datasets/Data JSON/weather_test.json", "r") as test_in:
    data = json.load(test_in)

    for obj in data["test"]:
        data_test.append(obj["Data"])
        label_test.append(float(obj["Target"]))

print("\n\n\nTesting data is\n")
print(data_test)
print(label_test)

sns.distplot(label_train)
sns.distplot(label_test)
plt.title("Weather Data Histogram Blue: Training, Orange: Testing")
plt.show()

# Ready the SVM
svm = SVC(kernel="linear", C=1.0, random_state=42)

# Train our model
svm.fit(data_train, label_train)

# Save our trained model using dill for production
with open('../API/weather_trained.pk', 'wb') as file:
    pickle.dump(svm, file)

# Try out a little prediction
prediction = svm.predict(data_test)
print("\n\n", prediction)

'''
    Scoring bit not needed while deploying the app
    Will be removed in production
'''
# Time to test if all of this went to waste or not
test_score = svm.score(data_test, label_test)

# Print our test score
print("\n\nResult of our modeling is {0:.1f}%".format(test_score * 100))

report = classification_report(label_test, prediction)
print(report)

# EOF
