import argparse
import pprint
import sys
import gensim
import train_word2vec_model

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Word2Vec model building')
    parser.add_argument('--model_path', action='store', help='the path to the model')
    params = vars(parser.parse_args(args))
    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_path = params['model_path']

    train_word2vec_model.enable_verbose_training(sys.argv[0])

    try:
        model = gensim.models.Word2Vec.load_word2vec_format(input_path, binary=True)
        # this raises an exception if the model type is different..
    except Exception:
        # just use the other mothod of loading..
        model = gensim.models.Word2Vec.load(input_path)

    model.accuracy('questions-words.txt')

    pprint.pprint(model.most_similar('computer'))
    pprint.pprint(model.most_similar('cyberspace'))
    pprint.pprint(model.most_similar('stupid'))
    # this fails weirdly. what is similar_cosmul anyhow?
    #pprint.pprint(model.most_similar_cosmul('berlin', 'spain'))
    print(model.similarity('computer', 'cyberspace'))
    print(model.similarity('question', 'answer'))
    print(model.n_similarity(['i', 'like', 'brown', 'turtles'], ['i', 'like', 'dark', 'brown', 'turtles']))
    pprint.pprint(model.most_similar(positive=['computer'], negative=['keyboard'], topn=10))
    pprint.pprint(model.doesnt_match('computer keyboard internet cigarette'.split()))
