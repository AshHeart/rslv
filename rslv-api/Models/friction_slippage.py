"""
    Our second of two models

    This model accepts data from our weather model and combines it with friction
    coefficient values to determine slippage, slippage is determined using a confidence value
    ranging from 0-1 in increments of 0.1

    Classifier used: Support Vector Machines
    Training Data: Friction data pulled from the file "rslv/Datasets/Data JSON/friction_train.json"
    Testing Data: Friction data pulled from the file "rslv/Datasets/Data JSON/friction_test.json"

    Samples Used:
        Training: 400
        Testing: 50

    TODO: "Modify for deployment"
"""

from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn import tree
import seaborn as sns
import matplotlib.pyplot as plt

# For deploying our trained model
import dill as pickle

import json

# Training Data Variables
data_train = []
label_train = []

# Testing data holders
data_test = []
label_test = []

with open("../Datasets/Data JSON/friction_train.json", "r") as train_in:
    data = json.load(train_in)

    for obj in data["train"]:
        data_train.append(obj["Data"])
        label_train.append(obj["Target"])

print("\n\nTraining Data is\n")
print(data_train)
print(label_train)

with open("../Datasets/Data JSON/friction_test.json", "r") as test_in:
    data = json.load(test_in)

    for obj in data["test"]:
        data_test.append(obj["Data"])
        label_test.append(obj["Target"])

print("\n\nTesting Data is\n")
print(data_test)
print(label_test)

# sns.distplot(label_train, label="Friction Training Data Histogram")
# sns.distplot(label_test, label="Friction Testing Data Hostogram")
# plt.title("Friction Data Histogram Blue: Training, Orange Testing")
# plt.show()

# Ready the SVM
svm = SVC(kernel='linear', C=1.0, random_state=42)
#svm = tree.DecisionTreeClassifier(criterion='gini', max_depth=6, min_samples_split=7)

# Train our model
clf.fit(data_train, label_train)
svm.fit(data_train, label_train)

# Save our trained model using dill for production
with open('../API/friction_trained.pk', 'wb') as file:
    pickle.dump(clf, file)

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

#EOF