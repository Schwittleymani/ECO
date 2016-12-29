import argparse
import pprint
import glob
import sys
import gensim
import util
import numpy
import json
import os
from sklearn.manifold import TSNE

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Word2Vec model building')
    parser.add_argument('--model_path', action='store', help='the path to the model')
    parser.add_argument('--txt_path', action='store', help='path containing text files which are all loaded')
    parser.add_argument('--output_file', action='store', help='the text file to store all vectors in')
    params = vars(parser.parse_args(args))
    return params

class LineVectorCombination(object):
    vector = 0
    sentence = 0

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_path = params['model_path']

    util.enable_verbose_training(sys.argv[0])
    try:
        model = gensim.models.Word2Vec.load_word2vec_format(input_path, binary=True)
        # this raises an exception if the model type is different..
    except Exception:
        # just use the other mothod of loading..
        model = gensim.models.Word2Vec.load(input_path)

    txt_path = params['txt_path']

    data_300d = []

    originals = []
    original_vectors = []
    original_sentences = []

    text_files = glob.glob(txt_path + '/*.txt')
    for file in text_files:
        for line in open(file, 'r'):
            vector_words = []
            word_count = 0
            for word in line.split():
                try:
                    vector_words.append(model[word])
                    word_count += 1
                except:
                    pass
                    # skip vocab unknown word
            if word_count > 5:
                vector = gensim.matutils.unitvec(numpy.array(vector_words).mean(axis=0))
                combined = LineVectorCombination()
                combined.sentence = line
                combined.vector = vector
                originals.append(combined)
                original_vectors.append(vector)
                original_sentences.append(line)
                vlist = vector.tolist()
                intlist = []
                for number in vlist:
                    intnumber = int(number*10000)
                    intlist.append(intnumber)
                data_300d.append({"sentence": line, "point": intlist})

    output_file = params['output_file']

    # X = numpy.array(original_vectors)
    # tsne = TSNE(n_components=2, learning_rate=200, perplexity=20, verbose=2).fit_transform(X)
    #
    # data_2d = []
    # for i, f in enumerate(original_sentences):
    #     point = [(tsne[i, k] - numpy.min(tsne[:, k]))/(numpy.max(tsne[:, k]) - numpy.min(tsne[:, k])) for k in range(2)]
    #     data_2d.append({"sentence": os.path.abspath(original_sentences[i]), "point": point})

    with open(output_file, 'w') as outfile:
        #json.dump(data_2d, outfile)
        json.dump(data_300d, outfile)
