import gensim
import math
import sys
import os
import pathlib
import glob
import argparse
import multiprocessing
import logging
import pprint

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
        text_files = glob.glob(self.dirname + '/*.txt')
        for file in text_files:
            for line in open(file, 'r'):
                # compare two models which are trained with the next line toggled
                line = line.lower()
                yield line.split()

def get_last_dir_from_path(path):
    list = path.split('/')
    if path.endswith('/'):
        out = list[-2]
    else:
        out = list[-1]
    return out

def enable_verbose_training():
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

def train_model(folder_path):
    model = gensim.models.Word2Vec(
        Sentence(folder_path),
        # the more training data, the higher the size
        size=400,
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

def export_model(input_path):
    # the input path is used for constructing the filename of the model
    model_filename = get_last_dir_from_path(input_path) + '.model'
    # file exists already in current directory?
    if pathlib.Path(model_filename).is_file():
        # y/n choice to overwrite
        user_input = input('Overwrite model file ' + model_filename + '? [y/(n)]')
        if 'y' in user_input:
            model.save(model_filename)
            print('Saved model: ' + model_filename)
        else:
            print('NOT saved model. File already exists.')
    else:
        model.save(model_filename)
        print('Saved model: ' + model_filename)


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_path = params['input_path']
    verbose = params['verbose']

    if verbose:
        enable_verbose_training()

    model = train_model(input_path)

    pprint.pprint(model.most_similar('computer'))
    pprint.pprint(model.most_similar('cyberspace'))
    pprint.pprint(model.most_similar('stupid'))
    pprint.pprint(model.similarity('computer', 'cyberspace'))
    pprint.pprint(model.similarity('question', 'answer'))
    pprint.pprint(model.most_similar(positive=['computer'], negative=['keyboard'], topn=10))
    export_model(input_path)
