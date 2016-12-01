from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class meany(object):
    
    def __init__(self, text):
        self.text = text
        self.tokened = word_tokenize(text)
        self.filtered = [word for word in self.tokened if word.lower() not in set(stopwords.words('english')]
        self.ps = PorterStemmer()
        self.stemmed = [self.ps.stem(word) for word in self.filtered]
        self.pos = pos_tag(self.filtered)
        self.mean = False
        self.mean_lvl = None
        self.analyzed = False
    
    def is_mean(self):
        '''
        Determines if the self.text is mean or not
        self.text -> bool
        '''
        if '@' in self.text:
            self.mean = True
            self.analyzed = True
            
    def how_mean(self):
        '''
        determines the level of meanness on a scale of 1 to 10
        self.text -> int
        '''
        if not self.analyzed:
            self.is_mean()
        if self.mean:
            self.mean_lvl = 10