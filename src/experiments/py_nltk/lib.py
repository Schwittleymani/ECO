from nltk.tokenize import word_tokenize
from nltk import pos_tag

def tag(string):
    s_type = type(string)
    #print string, 
    if s_type == list:
        return pos_tag(string)
    elif s_type == str or s_type == unicode:
        sent = word_tokenize(string)
        #print sent,len(sent)
        if len(sent) > 1:
            return pos_tag(sent)
        else:
            #print pos_tag(sent)
            return pos_tag(sent)[0]
        
        
class Tester:
    
    def test_tag():
        print(['this','is','funky'])
        print('this is funky')
        print('funky')
        