from gensim.models.doc2vec import Doc2Vec
import argparse
import pprint
import sys
import util

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Doc2Vec model building')
    parser.add_argument('--model_path', action='store', help='the path to the model')
    params = vars(parser.parse_args(args))
    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_path = params['model_path']

    util.enable_verbose_training(sys.argv[0])

    try:
        model = Doc2Vec.load_word2vec_format(input_path, binary=True)
        # this raises an exception if the model type is different..
    except Exception:
        # just use the other mothod of loading..
        model = Doc2Vec.load(input_path)
    print(len(model.vocab))

    pprint.pprint(model.most_similar('computers are cool'))
    pprint.pprint(model.most_similar('computers are stupid'))