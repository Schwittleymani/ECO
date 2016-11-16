import sys
import os
import argparse
import gensim
import numpy as np
import scipy.spatial.distance

class Sentence(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                line_low = line.lower()
                yield line_low.split()

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure the irc clients')
    parser.add_argument('--path', action='store', help='the path to a folder containing text files')
    params = vars(parser.parse_args(args))
    return params

def avg_feature_vector(words, model, num_features):
    # function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float64")
    nwords = 0

    # list containing names of words in the vocabulary
    # index2word_set = set(model.index2word) this is moved as input param for performance reasons
    for word in words:
        if word in model.vocab:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])
        else:
            print('not in vocabulary: ' + word)

    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    features = 300

    path = params['path']
    sentences = Sentence(path)
    model_selftrained = gensim.models.Word2Vec(sentences, min_count=5, size=features, workers=8)

    sentence_a = 'This attribution is putting the other in a condition of authority and assurance'
    sentence_b = 'condition of a superior joke, that by rise up is to say the promotion of new statuses, new powers.'
    sentence_c = 'Feels stange, of course, being perceived as not human.'
    sentence_d = 'of human expression'
    sentence_e = 'This joke is putting other into a weird condition'

    sentences = [sentence_a, sentence_b, sentence_c, sentence_d, sentence_e]
    for index, sentence in enumerate(sentences):
        _sentence = sentence.replace('.', '')
        _sentence = _sentence.lower()
        sentences[index] = _sentence.replace(',', '')

    sentence_a_vec = avg_feature_vector(sentences[0].split(), model=model_selftrained, num_features=features)
    sentence_b_vec = avg_feature_vector(sentences[1].split(), model=model_selftrained, num_features=features)
    sentence_c_vec = avg_feature_vector(sentences[2].split(), model=model_selftrained, num_features=features)
    sentence_d_vec = avg_feature_vector(sentences[3].split(), model=model_selftrained, num_features=features)
    sentence_e_vec = avg_feature_vector(sentences[4].split(), model=model_selftrained, num_features=features)

    sena_senb_similarity = 1 - scipy.spatial.distance.cosine(sentence_a_vec, sentence_b_vec)
    sena_self_similarity = 1 - scipy.spatial.distance.cosine(sentence_a_vec, sentence_a_vec)
    sena_sene_similarity = 1 - scipy.spatial.distance.cosine(sentence_a_vec, sentence_e_vec)
    print(sena_senb_similarity)
    print(sena_self_similarity)
    print(sena_sene_similarity)