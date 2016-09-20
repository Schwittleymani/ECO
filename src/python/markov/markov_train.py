import sys
import argparse

from markov_wrapper import MarkovWrapper


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--input', action='store', help='the path to the input text file')
    parser.add_argument('--prime', action='store', help='what is the beginning of the sampled text')
    parser.add_argument('--model_save_path', action='store', default=None, help='path to save the exported models to')
    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_text_path = params['input']
    prime = params['prime']
    model_save_path = params['model_save_path']

    print('Running LSTM with parameters:')
    print('----------------------------------------')
    print('Training input file: ' + input_text_path)
    print('Sampling with prime text: ' + prime)
    print('----------------------------------------')

    markov = MarkovWrapper()
    markov.train(input_path=input_text_path, state_size=2)
    while True:
        input = raw_input('input: ')
        print(markov.sample_short(140))

        try:
            print('markov.sample')
            print(markov.sample(prime=input, length=140))
        except KeyError:
            print('KeyError')