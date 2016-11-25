
class meany(object):
    
    def __init__(self, text):
        self.text = text
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