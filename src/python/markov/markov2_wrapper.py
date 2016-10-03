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
        self.name = None
        print('Loading from ' + input_path)
        self.markov = Markov(open(input_path))

    def sample(self, input_text, length):
        input_text_list = input_text.split()

        # there need to be at least two words input
        if len(input_text_list) == 0:
            input_text_list.append(self.markov.get_random_word())
        if len(input_text_list) == 1:
            input_text_list.append(self.markov.get_random_word())

        times_to_try = 10

        output = self.__sample_implementation(input_text_list, length=length)

        while times_to_try > 0 and output is None:
            input_text_list[1] = self.markov.get_random_word()
            output = self.__sample_implementation(input_text_list=input_text_list, length=length)
            times_to_try -= 1

        if output is None:
            return 'no_answer_markov'
        else:
            return output

    def __sample_implementation(self, input_text_list, length):
        try:
            text = self.markov.generate_markov_text(input_text_list, length)

            # remove the last two words from the input string because they'll be doubled otherwise
            del input_text_list[-1]
            del input_text_list[-1]

            output = ' '.join(input_text_list)
            output += ' ' + text
            return output
        except KeyError:
            return  None


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