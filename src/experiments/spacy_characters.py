import spacy
import os
import codecs
from collections import Counter, defaultdict

filename = '/mnt/drive1/data/eco/NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt'
if not os.path.isfile(filename):
    print "file",filename,'is not there...'


nlp = spacy.load('en')

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().decode('utf-8')

# open the file
text = read_file(filename)
# Process `text` with Spacy NLP Parser
processed_text = nlp(text)

def write_lists_to_file(lists):
	with codecs.open('character_file.txt','w','utf-8') as out:
		for al in lists:
			out.write(al[0]+','+str(al[1])+'\n')


def find_character_occurences(processed_txt):
    """
    Return a list of actors from `doc` with corresponding occurences.
    """
    total_len = len(processed_text)
    characters = Counter()
    
    index = 0
    for ent in processed_txt.ents:
        if ent.label_ == 'PERSON':
            characters[ent.lemma_] += 1
        if index % (total_len/10) == 0:
            print '*',
        index += 1
            
    return characters

characters = find_character_occurences(processed_text)
write_lists_to_file(characters)