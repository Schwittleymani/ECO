# 1 used for loading or saving
import gensim
model_file = '/home/ramin/projects/ECO/src/python/modelbuilder/parsed_v3_valid.doc2vec'

# 2 Build sentence list (each sentence needs at least 1 tag)
filename = '/home/marcel/drive/data/eco/NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt'

sentences = []
from random import shuffle

for uid, line in enumerate(open(filename)):
    ls = gensim.models.doc2vec.LabeledSentence(words=line.split(), tags=['SENT_%s' % uid])
    sentences.append(ls)
print(len(sentences),'sentences')




# 4 Loading the model

model_loaded = gensim.models.Doc2Vec.load(model_file)


# 6 Tiny helper
import re

def nice_print(tagged_doc):
    sentence = sentences[int(tagged_doc[0][5:])][0]
    str =  ' '.join(sentence)
    pattern = re.compile('\s.\s')
    shift = 0
    for ma in pattern.finditer(str):
        str = str[:ma.start(0)-shift]+ma.group(0)[1:]+ str[ma.end(0)-shift:]
        shift +=1
    if str[-2] == ' ':
        str = str[:-2] + str[-1:]
    return str

def print_similar(similar):
    return nice_print(similar)

def print_index(index):
    sentence = ' '.join(sentences[index][0])
    return sentence
    
def get_similar_index(similar):
    return int(similar[0][5:])
    
    
def equal_word_lists(index1, index2):
    wl1 = sentences[index1][0]
    wl2 = sentences[index2][0]
    if len(wl1) != len(wl2):
        return False
    else:
        for i in range(len(wl1)):
            if wl1[i] != wl2[i]:
                return False
    return True


# this is a duplicate filtering
filtered_out = set()
similar_thresh = 0.95

le = len(sentences)

for index, sentence in enumerate(sentences):
    if index % 100 == 0:
        print '---',str(index)+'/'+str(le)+'---'
    tag = sentence[1][0]
    sentence_printed = False
    if index in filtered_out:
        continue
    sims = model_loaded.docvecs.most_similar(tag) # get similarity by the tag
    for sim in sims:
        if sim[1] > similar_thresh:
            if equal_word_lists(index,get_similar_index(sim)):
                filtered_out.add(get_similar_index(sim))


output_file = '/home/ramin/drive/data/eco/NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid_duplicates_killed.txt'

with open(output_file,'w') as output:
    for index, sentence in enumerate(sentences):
        if index not in filtered_out:
            output.write(print_index(index))
