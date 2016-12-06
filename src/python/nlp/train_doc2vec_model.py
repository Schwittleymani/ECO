from gensim.models.doc2vec import Doc2Vec, LabeledSentence
import argparse
import multiprocessing
import sys
import math

import util

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Doc2Vec model building')
    parser.add_argument('--input_path', action='store', help='the path to a folder containing sentence txt file')
    parser.add_argument('--verbose', action='store_true', help='toggle to enable verbose output of training process')
    params = vars(parser.parse_args(args))
    return params

class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for uid, line in enumerate(open(self.filename)):
            # compare two models which are trained with the next line toggled
            line = line.lower()
            yield LabeledSentence(words=line.split(), labels=['SENT_%s' % uid])

def train_model(folder_path):
    model = Doc2Vec(
        dm=0, dbow_words=1,
        # the more training data, the higher the size. google model uses 300
        size=200,
        # drop all words which occur less than 5 times
        window=8, min_count=19, iter=10,
        workers=multiprocessing.cpu_count()
    )
    sentences = LabeledLineSentence(folder_path)
    model.build_vocab(sentences)
    model.train(sentences)
    #model.build_vocab(sentences)
    #for epoch in range(10):
    #    model.train(sentences)
    #    model.alpha -= 0.002  # decrease the learning rate
    #    model.min_alpha = model.alpha  # fix the learning rate, no decay

    model.init_sims(replace=True)
    print('Finished training: ' + str(model) + ' Filesize:', str(round(model.estimate_memory()['total'] / (math.pow(1024, 2)))) + 'mb')
    return model

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_path = params['input_path']
    verbose = params['verbose']

    if verbose:
        util.enable_verbose_training(sys.argv[0])

    model = train_model(input_path)
    util.export_model(model, input_path, '.d2vmodel')