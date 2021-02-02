# Actual implementation of Naive Bayes applied in a spam detection app
import os
import glob
import numpy as np
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer


e_mails, labels = [], []

# Load spam files from our dataset
file_path = 'enron1/spam/'
for fname in glob.glob(os.path.join(file_path, '*.txt')):
    with open(fname, 'r', encoding = "ISO-8859-1") as infile:
        e_mails.append(infile.read())
        labels.append(1)

#Load proper e_mails
file_path = 'enron1/ham/'
for fname in glob.glob(os.path.join(file_path, '*.txt')):
    with open(fname, 'r', encoding = "ISO-8859-1") as infile:
        e_mails.append(infile.read())
        labels.append(0)

'''Test Code will be commented in production
print(len(e_mails))
print(len(labels))
'''


#Clean the raw data
def letters_only(astr):
    return astr.isalpha()

all_names = set(names.words())
lemmatizer = WordNetLemmatizer()

def clean_text(docs):
    cleaned_docs = []
    for doc in docs:
        cleaned_docs.append(
            ' '.join([lemmatizer.lemmatize(word.lower())
                for word in doc.split()
                    if letters_only(word)
                        and word not in all_names
            ])
        )

    return cleaned_docs

cleaned_emails = clean_text(e_mails)

'''TestCode will be commented in production
print(cleaned_emails[10])
'''


#Time to remove stop words and extract feaatures
cv = CountVectorizer(stop_words = "english", max_features = 500)
term_docs = cv.fit_transform(cleaned_emails)

'''TestCode will be commented in production
print(term_docs[0])
feature_names = cv.get_feature_names()
print(feature_names[465])
feature_mapping = cv.vocabulary_
'''


#Building and training our model
    #First, group the data by labels
def get_label_index(labels):
    from collections import defaultdict

    label_index = defaultdict(list)

    for index, label in enumerate(labels):
        label_index[label].append(index)

    return label_index

label_index = get_label_index(labels)

    #Next calculate our prior
def get_prior(label_index):
    prior = {label: len(index) for label, index in label_index.items()}
    total_count = sum(prior.values())

    for label in prior:
        prior[label] /= float(total_count)

    return prior

prior = get_prior(label_index)

    #And our likelihood
def get_likelihood(term_document_matrix, label_index, smoothing = 0):
    likelihood = {}

    for label, index in label_index.items():
        likelihood[label] = term_document_matrix[index, :].sum(axis = 0) + smoothing
        likelihood[label] = np.asarray(likelihood[label])[0]
        total_count = likelihood[label].sum()
        likelihood[label] = likelihood[label] / float(total_count)

    return likelihood

smoothing = 1
likelihood = get_likelihood(term_docs, label_index, smoothing)

'''TestCode will be commented in production
print(len(likelihood[0]))

print(likelihood[0][:5])
'''


#Our posterior for new data
def get_posterior(term_document_matrix, prior, likelihood):
    num_docs = term_document_matrix.shape[0]
    posteriors = []

    for i in range(num_docs):
        posterior = {key: np.log(prior_label) for key, prior_label in prior.items()}

        for label, likelihood_label in likelihood.items():
            term_document_vector = term_document_matrix.getrow(i)
            counts = term_document_vector.data
            indices = term_document_vector.indices

            for count, index in zip(counts, indices):
                posterior[label] += np.log(likelihood_label[index]) * count

        min_log_posterior = min(posterior.values())

        for label in posterior:
            try:
                posterior[label] = np.exp(posterior[label] - min_log_posterior)
            except:
                posterior[label] = float('inf')

        sum_posterior = sum(posterior.values())

        for label in posterior:
            if posterior[label] == float('inf'):
                posterior[label] = 1.0
            else:
                posterior[label] /= sum_posterior

        posteriors.append(posterior.copy())

    return posteriors


email_tests = [
'''Subject: flat screens
hello,
please call or contact regarding the other flat screens
requested.
trisha tlapek - eb 3132 b
michael sergeev - eb 3132 a
also the sun blocker that was taken away from eb 3131 a.
trisha should two monitors also michael.
thanks
kevin moore''',
'''Subject: having problems in bed ? we can help !
cialis allows men to enjoy a fully normal sex life without
having to plan the sexual act .
if we let things terrify us, life will not be worth living
brevity is the soul on lingerie
suspicion always haunnts the guilty mins . '''
]

cleaned_text = clean_text(email_tests)
term_doc_test = cv.transform(cleaned_text)
posterior = get_posterior(term_doc_test, prior, likelihood)
print(posterior)


'''Time to evaluate our classifier performance'''
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(cleaned_emails, labels, test_size = 0.33, random_state = 42)

print(len(x_train), len(y_train))
print(len(x_test), len(y_test))

term_docs_train = cv.fit_transform(x_train)
label_index = get_label_index(y_train)
prior = get_prior(label_index)
likelihood = get_likelihood(term_docs_train, label_index, smoothing)

term_docs_test = cv.transform(x_test)
posterior = get_posterior(term_docs_test, prior, likelihood)

correct = 0.0
for pred, actual in zip(posterior, y_test):
    if actual == 1:
        if pred[1] >= 0.5:
            correct += 1
    elif pred[0] > 0.5:
        correct += 1

print('The accuracy on {0} testing samples is: {1:.1f}%'.format(len(y_test), correct / len(y_test) * 100
))


'''Use the built in classifier'''
from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB(alpha = 1.0, fit_prior = True)

clf.fit(term_docs_train, y_train)

prediction_prob = clf.predict_proba(term_docs_test)
print(prediction_prob[0:10])

prediction = clf.predict(term_docs_test)
print(prediction[:10])

accuracy = clf.score(term_docs_test, y_test)
print("The accuracy using MultinomialNB is {0:.1f}%".format(accuracy * 100))
