import sys
import os
import argparse
import time
import gensim
import random
sys.path.insert(0, '../irc/markov_python3.py')
import markov
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
        log.append((random_a, random_b, similarity))
    t1 = time.time()
    print('calculating all vectors took ' + str(t1-t0) + 's')
    log.sort(key=lambda log: log[2], reverse=True)
    print('Best results:')
    for i in range(10):
        print('Index: ' + str(i))
        print(log[i][0])
        print(log[i][1])
        print('with similarity: ' + str(log[i][2]))

def train_markovs(path, max_markov=30):
    markovs = []
    for fname in os.listdir(path):
        if len(markovs) > max_markov:
            break
        print('Start training markov from ' + fname)
        markov_chain = markov.Markov(prefix=fname)
        line_count = 0
        for line in open(os.path.join(path, fname)):
            line_low = line.lower()
            markov_chain.add_line_to_index(line_low.split())
            line_count += 1
        print('Done training markov from ' + fname)
        if line_count > 200:
            markovs.append(markov_chain)
    return markovs

def third_testing(path, google_path, features):
    markovs = train_markovs(path=path, max_markov=120)
    print('Done Training Markovs')
    model = gensim.models.Word2Vec.load_word2vec_format(google_path, binary=True)
    print('Done loading Google model')
    model_selftrained = gensim.models.Word2Vec(Sentence(path), min_count=5, size=features, workers=8)
    print('Done training own model')

    _t0 = time.time()
    # loading all lines for comparison
    lines_vectors_google = []
    lines_vectors_own = []
    for fname in os.listdir(path):
        for line in open(os.path.join(path, fname)):
            line_low = line.lower()
            vector_google = avg_feature_vector(line_low.split(), model=model_selftrained, num_features=features)
            vector_own = avg_feature_vector(line_low.split(), model=model, num_features=features)
            lines_vectors_google.append((line_low, vector_google))
            lines_vectors_own.append((line_low, vector_own))
    _t1 = time.time()
    print('Calculating all vectors on google/own models for sentences from own corpus done')
    print('That took ' + str(int(_t1-_t0)) + 's. It was done for ' + str(len(lines_vectors_google)) + ' lines')
    markov_dict = {}
    for markov in markovs:
        generated_sentences = []
        print('----------------------------------------')
        print(markov.prefix)
        for i in range(10):
            t0 = time.time()
            sentence = markov.generate(max_words=100)

            sentence_vec_google = avg_feature_vector(' '.join(sentence).lower().split(), model=model_selftrained, num_features=features)
            sentence_vec_own = avg_feature_vector(' '.join(sentence).lower().split(), model=model, num_features=features)

            # iterating through all vectors of all existing text lines from our corpus
            biggest_similarity_google = 0.0
            biggest_similarity_sentence_google = ''
            biggest_similarity_own = 0.0
            biggest_similarity_sentence_own = ''
            for index_corpus_line in range(len(lines_vectors_google)):
                vec_google = lines_vectors_google[index_corpus_line][1]
                vec_own = lines_vectors_own[index_corpus_line][1]
                similarity_google = 1 - scipy.spatial.distance.cosine(vec_google, sentence_vec_google)
                similarity_own = 1 - scipy.spatial.distance.cosine(vec_own, sentence_vec_own)

                if similarity_google > biggest_similarity_google:
                    biggest_similarity_google = similarity_google
                    biggest_similarity_sentence_google = lines_vectors_google[index_corpus_line][0]
                if similarity_own > biggest_similarity_own:
                    biggest_similarity_own = similarity_own
                    biggest_similarity_sentence_own = lines_vectors_own[index_corpus_line][0]

            t1 = time.time()

            print('----------------------------------------')
            print('markov: ' + ' '.join(sentence))
            print('closest via google: ' + biggest_similarity_sentence_google)
            print('closest via own model: ' + biggest_similarity_sentence_own)
            #print('Calculating this took: ' + str(int(t1-t0)) + 's')
            generated_sentences.append(sentence)
        markov_dict[markov] = generated_sentences

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
    elif method in 'markov':
        # loading google model and own model (for comparing)
        third_testing(path=path, google_path=google_path, features=features)