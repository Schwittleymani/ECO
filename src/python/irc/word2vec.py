import sys
import os
import argparse
import time
import gensim
import random
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
    parser.add_argument('--google_path', action='store', help='the path to the pretrained google model')
    parser.add_argument('--method', action='store', help='the test function to use')

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
        #else:
        #    print('not in vocabulary: ' + word)

    if nwords > 0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

def first_testing(model_selftrained, features):
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
    sena_send_similarity = 1 - scipy.spatial.distance.cosine(sentence_a_vec, sentence_d_vec)
    print(sena_senb_similarity)
    print(sena_self_similarity)
    print(sena_sene_similarity)
    print(sena_send_similarity)

def second_training(google_model, path, features):
    lines = []
    for fname in os.listdir(path):
        for line in open(os.path.join(path, fname)):
            line_low = line.lower()
            lines.append(line_low)
    log = []
    print('Collected ' + str(len(lines)) + ' lines.')
    t0 = time.time()
    for i in range(100000):
        random_a = random.choice(lines)
        random_b = random.choice(lines)
        random_a_vec = avg_feature_vector(random_a.split(), model=google_model, num_features=features)
        random_b_vec = avg_feature_vector(random_b.split(), model=google_model, num_features=features)
        similarity = 1 - scipy.spatial.distance.cosine(random_a_vec, random_b_vec)
        #print('a: ' + random_a)
        #print('b: ' + random_b)
        #print('sim: ' + str(similarity))
        log.append((random_a, random_b, similarity))
    t1 = time.time()
    print('calculating all vectors took ' + str(t1-t0) + 's')
    log.sort(key=lambda scores: scores[2], reverse=True)
    print('Best results:')
    for i in range(10):
        print('Index: ' + str(i))
        print(log[i][0])
        print(log[i][1])
        print('with similarity: ' + str(log[i][2]))

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    features = 300
    method = params['method']
    path = params['path']
    google_path = params['google_path']
    if method in 'first':
        sentences = Sentence(path)
        model_selftrained = gensim.models.Word2Vec(sentences, min_count=5, size=features, workers=8)
        first_testing(model_selftrained, features=features)
    elif method in 'google':
        t0 = time.time()
        model = gensim.models.Word2Vec.load_word2vec_format(google_path, binary=True)
        t1 = time.time()
        print('Loading the google model took ' + str(t1-t0) + 's')
        second_training(google_model=model, path=path, features=features)