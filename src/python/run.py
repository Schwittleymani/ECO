import markov.markov2_wrapper
import keras_lstm.lstm_wrapper
import webserver

import argparse
import sys


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--input', action='store', help='the path to the input text file')
    params = vars(parser.parse_args(args))

    return params


class Generator(object):
    def __init__(self):
        pass

    def init_markov(self, input_text_path):
        self.markov = markov.markov2_wrapper.Markov2Wrapper(input_text_path)

    '''
    input_text_path: path to text file to train on
    maxlen: the maximum amount of input characters to use
    iterations: the number of iterations to train
    epochs: numbers of epochs to train
    steps: how many character combinations to check
    save_every: after how many iterations to save the model temporary (0 -> not saving)
    '''
    def init_keras_lstm(self, input_text_path, maxlen=100, iterations=3, epochs=5, steps=2, save_every=0):
        self.lstm = keras_lstm.lstm_wrapper.LSTMWrapper(maxlen=maxlen, step=steps)
        self.lstm.load(path=input_text_path)
        self.lstm.train(iterations=iterations, epochs=epochs, model_save_path=None, save_every=save_every)

    def sample_markov(self, input, length=50):
        return self.markov.sample(input_text=input, length=length)

    def sample_keras_lstm(self, input, diversity=0.3, length=50):
        return self.lstm.sample(diversity=diversity, seed=input, output_length=length)


'''
## this is the main entry point for the software running on lyrik

    KERAS_BACKEND=tensorflow python run.py --input *textfile*
'''
if __name__ == '__main__':

    params = process_arguments(sys.argv[1:])
    input_text_path = params['input']

    generator = Generator()
    generator.init_markov(input_text_path=input_text_path)
    generator.init_keras_lstm(input_text_path=input_text_path)

    while True:
        input = raw_input('input: ')

        markov_result = generator.sample_markov(input=input)
        keras_lstm_result = generator.sample_keras_lstm(input=input)

        print('--- Result ---')
        print('Markov Chain: ' + markov_result)
        print('Keras LSTM: ' + keras_lstm_result)