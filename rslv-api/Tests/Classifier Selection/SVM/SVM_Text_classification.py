''' Here we try to classify news data from our 20 newsgroups nltk dataset usign a subcategory of SVM'''

'''All our imports'''
from sklearn.datasets import fetch_20newsgroups
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

'''Our functions'''
#We only need words with alphabets
def letters_only(astr):
    return astr.isalpha()

all_names = set(names.words())
lemmatizer = WordNetLemmatizer()

#To clean our stuff
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

'''Data segregation'''
categories = ['comp.graphics', 'sci.space']
data_train = fetch_20newsgroups(subset = 'train', categories = categories, random_state = 42)
data_test = fetch_20newsgroups(subset = 'test', categories = categories, random_state = 42)

#Clean data after extraction
cleaned_train = clean_text(data_train.data)
cleaned_test = clean_text(data_test.data)

#Get labels after extraction
label_train = data_train.target
label_test = data_test.target

'''Test code wil be commented out in production
print(label_train, label_test)
print(cleaned_train, cleaned_test)
'''

'''Checking our data from imbalance'''
print(Counter(label_train))
print(Counter(label_test))

'''Extract tf-idf from our data'''
tf_idf_vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, stop_words = 'english', max_features = 8000)

term_docs_train = tf_idf_vectorizer.fit_transform(cleaned_train)
term_docs_test = tf_idf_vectorizer.transform(cleaned_test)

'''Test code will be commented in production'''
print(term_docs_train)
print(term_docs_test)

svm = SVC(kernel = 'linear', C = 1.0, random_state = 42)

svm.fit(term_docs_train, label_train)

test_score = svm.score(term_docs_test, label_test)

print("Result of our modeling is {0:.1f}%".format(test_score * 100))
