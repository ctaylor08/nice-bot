import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import DecisionTreeClassifier, MaxentClassifier, ClassifierI
from statistics import mode
import random


with open('mean.txt') as f:
    data = f.read()
    mean_tweets = [(line.lower(), 1) for line in data.split('\n')]
    mean_tkn_fltrd = [w.lower() for w in word_tokenize(data) if w.lower() not in set(stopwords.words('english'))]
    
with open('nice.txt') as f:
    data = f.read()
    nice_tweets = [(line.lower(), 0) for line in data.split('\n')]
    nice_tkn_fltrd = [w.lower() for w in word_tokenize(data) if w.lower() not in set(stopwords.words('english'))]
    
all_tweets = mean_tweets + nice_tweets
all_tkn_fltrd = mean_tkn_fltrd + nice_tkn_fltrd

all_dist = nltk.FreqDist(all_tkn_fltrd)

word_features = list(all_dist.keys())

def find_features(doc):
    words = word_tokenize(doc)
    features = {}
    for w in word_features:
        features[w] = (w in words)
        
    return features
    
featuresets = [(find_features(tweet), score) for (tweet, score) in all_tweets]
random.shuffle(featuresets)

half = int(len(featuresets)/2)

training_set = featuresets[:half]
testing_set = featuresets[half:]


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
        
        
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

#DT_classifier = DecisionTreeClassifier.train(training_set)
#print("DT_classifier accuracy percent:", (nltk.classify.accuracy(DT_classifier, testing_set))*100)

ME_classifier = MaxentClassifier.train(training_set)
print("ME_classifier accuracy percent:", (nltk.classify.accuracy(ME_classifier, testing_set))*100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

##SVC_classifier = SklearnClassifier(SVC())
##SVC_classifier.train(training_set)
##print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


voted_classifier = VoteClassifier(
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)
