from random import shuffle
import gensim

filename = '/home/marcel/drive/data/eco/NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt'

sentences = []

for uid, line in enumerate(open(filename)):
    ls = gensim.models.doc2vec.LabeledSentence(words=line.split(), tags=['SENT_%s' % uid])
    sentences.append(ls)
print(len(sentences),'sentences')

model = gensim.models.Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
print('building vocab') 
model.build_vocab(sentences)

base_alpha = model.alpha
base_min_alpha = model.min_alpha

for mepoch in range(2):
	model.alpha = base_alpha 
	model.min_alpha = base_min_alpha 	
	for epoch in range(10):
	    print('epoch',mepoch * 10 + epoch)
	    model.train(sentences)
	    model.alpha -= 0.002  # decrease the learning rate
	    model.min_alpha = model.alpha  # fix the learning rate, no decay

model_file = 'parsed_v3_valid.doc2vec'
model.save(model_file)
