from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.chat import eliza, iesha, rude,suntsu

def tag(string):
    """
    returns tagging for different types of inputs.
    sentence as a string > list of tags
    sentence as a list > list of tags
    word as string > tag
    """
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
        
def line_sentences(file_path):
    """
    return a list of lineSentences. breaks utf-8 ;(
    """
    #sfs = nltk.tokenize.stanford_segmenter.StanfordSegmenter("stanford-parser.jar")   
    raw = unicode(open(file_path).read(), errors='replace')
    #sent_tokenize_list = sfs.segment_sents(raw)
    sent_tokenize_list = sent_tokenize(raw)
    return sent_tokenize_list

def sentences_word_tokenized(lines):
    """
    breaks the line list into word lists
    """
    lines_tokenized = []
    for line in lines:
        lines_tokenized.append(word_tokenize(line))
        #lines_tokenized.append(map(lambda w : w.encode('ascii','ignore'),word_tokenize(line)))
    return lines_tokenized
        
def save_line_sentence_file(file_path, sentences):
    sentences = LineSentence(file_path)
    
def print_similarities(similarity_list):
    for similarity in similarity_list:
        print similarity[0].ljust(18),similarity[1]

def similarities_p(pos=[],neg=[],topn=10,doPrint = True):
    if doPrint: 
        print "pos:",pos,"neg:",neg
    similarities = model.most_similar(pos,neg,topn)
    if doPrint: print_similarities(similarities)
    return similarities
        
def word_similar_cosmul_p(model, word,topn=10, do_print = True,words_only = False):
    if do_print: print "word:",word
    similarities = model.similar_by_word(word,topn)
    if do_print: print_similarities(similarities)    
    if words_only:
        similarities = map(lambda sim : sim[0],similarities)
    return similarities  

def scaled_dispersion_plot(text,words,ignore_case=False, title = 'Lexical Dispersion Plot'):
    """
    kindof useless since i didnt figure out how to scale.
    google 'nltk dispersion_plot' and just call it...
    """
    from matplotlib import pylab
    text = list(text)
    words.reverse()
    
    words_to_comp = words
    text_to_comp = text
    
    ignore_case = False
    points= [(x,y) for x in range(len(text_to_comp))
            for y in range(len(words_to_comp))
            if text_to_comp[x] == words_to_comp[y]]
    
    if points:
        x,y = list(zip(*points))
    else:
        x = y = ()
    
    pylab.plot(x,y,'b|',scalex = 3,scaley=3)
    pylab.yticks(list(range(len(words))), words, color='b')
    pylab.ylim(-1,len(words))
    pylab.title(title)
    pylab.xlabel('word offset')
    pylab.show()

word2vec_model_files = {'english':'models/GoogleNews-vectors-negative300.bin.gz',
    'spanish':'models/SBW-vectors-300-min5.bin.gz'} 

def loadModel(language):
    from gensim import models
    import math
    model_file = word2vec_model_files.get(language, 'english')
    model = models.Word2Vec.load_word2vec_format(model_file, binary=True)
    model.init_sims(replace=True) # save memory
    print 'model memory size, gb:', model.estimate_memory()['total']/(math.pow(1024,3))
    return model

class Tester:
    
    def test_tag():
        print(['this','is','funky'])
        print('this is funky')
        print('funky')

class NltkChatbots:

    def __init__(self):
        self.bots = {'eliza':eliza.eliza_chatbot,'rude':rude.rude_chatbot,
            'iesha':iesha.iesha_chatbot,'suntsu':suntsu.suntsu_chatbot}

    def Bot(self, botname):
        return self.bots.get(botname,eliza.eliza_chatbot)

    def response(self, botname, input):
        return self.bots.get(botname,eliza.eliza_chatbot).respond(input)

def encode_phrase(text):
    return '_'.join(text)


# ```
# - nltk chatbot antwort
# - fct to cut, create phrases
# ```
#         