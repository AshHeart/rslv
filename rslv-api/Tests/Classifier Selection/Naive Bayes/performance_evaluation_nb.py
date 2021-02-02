from spam_detector import *

#First we check or calculate our confusion matrix
from sklearn.metrics import confusion_matrix

print("\n\nPerformance Metrics")
print("\nOur confusion matrix is {}\n".format(confusion_matrix(y_test, prediction, labels=[0, 1])))

#Next our Naive Bayes model's F1 score
from sklearn.metrics import precision_score, recall_score, f1_score

print("Precision Score is {}".format(precision_score(y_test, prediction, pos_label=1)))
print("Our Recall Score is {}".format(recall_score(y_test, prediction, pos_label=1)))
print("Our F1 score is {}".format(f1_score(y_test, prediction, pos_label=1)))

#trying out 0 for our positional label in f1 f1_score
print("Our F1 score with position label 0 is {}\n".format(f1_score(y_test, prediction, pos_label=0)))

#now calculate all in one using the built in classifier evaluator
from sklearn.metrics import classification_report

report = classification_report(y_test, prediction)
print(report)

#Advanced classifier performance evaluation methods: ROC or Receiver Operating Characteristics
# and AUC or Area Uder the Curve
pos_prob = prediction_prob[:, 1]

thresholds = np.arange(0.0, 1.2, 0.1)
true_pos, flase_pos = [0]*len(thresholds), [0]*len(thresholds)
for pred, y in zip(pos_prob, y_test):
    for i, threshold  in enumerate(thresholds):
        if pred >= threshold:
            if y == 1:
                true_pos[i] += 1
            else:
                flase_pos[i] += 1
        else:
            break

true_pos_rate = [tp / 516.0 for tp in true_pos]
false_pos_rate = [fp / 1191.0 for fp in flase_pos]

import matplotlib.pyplot as plt
plt.figure()
lw = 2
plt.plot(false_pos_rate, true_pos_rate, color='darkorange', lw=lw)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0,  1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Postivie Rate")
plt.title("Receiver Operating Characteristics")
plt.legend(loc="lower right")
plt.show()

#Compute exact AUC of our model
from sklearn.metrics import roc_auc_score
print(roc_auc_score(y_test, pos_prob))

#Based on performance now we tweak our model
from sklearn.model_selection import StratifiedKFold

k = 10
k_fold = StratifiedKFold(n_splits=k)
cleaned_emails_np = np.array(cleaned_emails)
labels_np = np.array(labels)

max_features_option = [2000, 4000, 8000]
smoothing_factor_option = [0.5, 1.0, 1.5, 2.0]
fit_prior_option = [True, False]
auc_record = {}

for train_indices, test_indices in k_fold.split(cleaned_emails, labels):
    x_train, x_test = cleaned_emails_np[train_indices], cleaned_emails_np[test_indices]

    y_train, y_test = labels_np[train_indices], labels_np[test_indices]

    for max_features in max_features_option:
        if max_features not in auc_record:
            auc_record[max_features] = {}

        cv = CountVectorizer(stop_words="english", max_features=max_features)
        term_docs_train = cv.fit_transform(x_train)
        term_doc_test = cv.transform(x_test)

        for smoothing in smoothing_factor_option:
            if smoothing not in auc_record[max_features]:
                auc_record[max_features][smoothing] = {}

            for fit_prior in fit_prior_option:
                clf = MultinomialNB(alpha=smoothing, fit_prior=fit_prior)
                clf.fit(term_docs_train, y_train)

                prediction_prob = clf.predict_proba(term_doc_test)
                pos_prob = prediction_prob[:, 1]

                auc = roc_auc_score(y_test, pos_prob)
                auc_record[max_features][smoothing][fit_prior] = auc + auc_record[max_features][smoothing].get(fit_prior, 0.0)

print("max_features       smoothing      fit       prior       auc".format(max_features, smoothing, fit_prior, auc/k))
for max_features, max_features_record in auc_record.items():
    for smoothing, smoothing_record in max_features_record.items():
        for fit_prior, auc in smoothing_record.items():
            print("{0}      {1}      {2}      {3:.4f}".format(max_features, smoothing, fit_prior, auc/k))
