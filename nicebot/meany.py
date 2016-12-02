from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
import os

f = open(os.path.join('sample_data', 'lr_classifier.pickle'), 'rb')
mean_classifier = pickle.load(f)
f.close()

f = open(os.path.join('sample_data', 'word_features.pickle'), 'rb')
word_features = pickle.load(f)
f.close()

def find_features(doc):
    words = word_tokenize(doc)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

class meany(object):
    
    def __init__(self, text):
        self.text = text
        self.features = find_features(self.text)
        self.mean = 0
    
    def is_mean(self):
        '''
        Determines if the self.text is mean or not
        self.text -> bool (1 or 0)
        '''
        self.mean = mean_classifier.classify(self.features)
