import gensim
import math
import sys
import glob
import argparse
import multiprocessing

import util

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Word2Vec model building')
    parser.add_argument('--input_path', action='store', help='the path to a folder containing sentence txt file')
    parser.add_argument('--verbose', action='store_true', help='toggle to enable verbose output of training process')
    params = vars(parser.parse_args(args))
    return params

class Sentence(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        if self.dirname.endswith('.txt'):
            for line in open(self.dirname, 'r'):
                # compare two models which are trained with the next line toggled
                line = line.lower()
                yield line.split()
        else:
            text_files = glob.glob(self.dirname + '/*.txt')
            for file in text_files:
                for line in open(file, 'r'):
                    # compare two models which are trained with the next line toggled
                    line = line.lower()
                    yield line.split()


def train_model(folder_path):
    model = gensim.models.Word2Vec(
        Sentence(folder_path),
        # the more training data, the higher the size. google model uses 300
        size=300,
        # drop all words which occur less than 5 times
        min_count=5,
        # no idea what negative does
        negative=5,
        window=10,
        workers=multiprocessing.cpu_count()
    )
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
    util.export_model(model, input_path, '.w2vmodel')
