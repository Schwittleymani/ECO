import sys
import argparse

from markov2 import Markov


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--input', action='store', help='the path to the input text file')
    parser.add_argument('--prime', action='store', default=None, help='what is the beginning of the sampled text')
    parser.add_argument('--model_save_path', action='store', default=None, help='path to save the exported models to')
    parser.add_argument('--length', action='store', default=None, help='amount of words to output')
    params = vars(parser.parse_args(args))

    return params


class Markov2Wrapper(object):

    def __init__(self, input_path):
        self.markov = Markov(open(input_path))

    def sample(self, input_text, length):
        text = self.markov.generate_markov_text(input_text.split(), length)

        input = input_text.split()
        del input[-1]
        del input[-1]

        output = ' '.join(input)
        output += ' ' + text
        return output

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_text_path = params['input']
    model_save_path = params['model_save_path']
    length = int(params['length'])

    markov = Markov2Wrapper(input_text_path)

    while True:
        input = raw_input('input: ')

        output = markov.sample(input, length)
        print(output)