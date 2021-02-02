'''Here we use svm on data subdivided into multiple categories'''
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report

categories = [
    'alt.atheism',
    'talk.religion.misc',
    'sci.space',
    'rec.sport.hockey',
    'sci.space',
    'rec.sport.hockey'
]

'''Our functions'''


# We only need words with alphabets
def letters_only(astr):
    return astr.isalpha()


all_names = set(names.words())
lemmatizer = WordNetLemmatizer()


# To clean our stuff
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


data_train = fetch_20newsgroups(subset='train', categories=categories, random_state=42)
data_test = fetch_20newsgroups(subset='test', categories=categories, random_state=42)

cleaned_train = clean_text(data_train.data)
cleaned_test = clean_text(data_test.data)

label_train = data_train.target
label_test = data_test.target

tf_idf_vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english', max_features=8000)

term_docs_train = tf_idf_vectorizer.fit_transform(cleaned_train)
term_docs_test = tf_idf_vectorizer.transform(cleaned_test)

svm = SVC(kernel='linear', C=1.0, random_state=42)

svm.fit(term_docs_train, label_train)

test_score = svm.score(term_docs_test, label_test)

print("Result of our modeling is {0:.1f}%".format(test_score * 100))

prediction = svm.predict(term_docs_test)
report = classification_report(label_test, prediction)
print(report)
