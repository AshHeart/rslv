import matplotlib.pyplot as plt
import seaborn as sns
import json

label_test = []
label_train = []

with open("../Datasets/Data JSON/friction_test.json", "r") as test_in:
    data = json.load(test_in)

    for obj in data["test"]:
        label_test.append(float(obj["Target"]))

with open("../Datasets/Data JSON/friction_train.json", "r") as test_in:
    data = json.load(test_in)

    for obj in data["train"]:
        label_train.append(float(obj["Target"]))

sns.distplot(label_test, label="Friction Testing Set", color="Red", axlabel="Friction Coefficients")
sns.distplot(label_train, label="Friction Training Set", color="Green",)
plt.title("Friction Training Data Histogram Red: Test Set  Green: Train Set")
plt.show()