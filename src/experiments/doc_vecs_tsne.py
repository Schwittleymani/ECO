import json, re, time, pickle, locale, os, socket, codecs, sys, bz2
from random import random, choice, randint, shuffle
import gensim
import numpy as np
from sklearn.manifold import TSNE

model_file = '/mnt/drive1/data/eco/doc2vec_models/parsed_v3_valid.doc2vec'
model = gensim.models.Doc2Vec.load(model_file)
tsne_model = TSNE(n_components=2, random_state=0)
tsne_res = tsne_model.fit_transform(model.docvecs)
tsne_res.tofile('tsne_res.txt')