import matplotlib.pyplot as plt
import seaborn as sns
import json

label_test = []
label_train = []

with open("../Datasets/Data JSON/weather_test.json", "r") as test_in:
    data = json.load(test_in)

    for obj in data["test"]:
        label_test.append(float(obj["Target"]))

with open("../Datasets/Data JSON/weather_train.json", "r") as test_in:
    data = json.load(test_in)

    for obj in data["train"]:
        label_train.append(float(obj["Target"]))

sns.distplot(label_test, label="Weather Testing Set", color="Blue", axlabel="Road Condition")
sns.distplot(label_train, label="Weather Training Set", color="Yellow",)
plt.title("Weather Training Data Histogram Blue: Test Set  Yellow: Train Set")
plt.show()