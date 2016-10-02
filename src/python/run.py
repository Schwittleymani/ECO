import postpreprocess.spell_check

import argparse
import sys

from generator import Generator
import webserver.server
import settings


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--keras_models_path', action='store',
                        help='the path to the folder that contains all trained keras lstm models')
    parser.add_argument('--markov_texts_path', action='store',
                        help='the path where text files lie in order to train the markov chains')
    parser.add_argument('--word_lstm_models_path', action='store',
                        help='the path where the models are stored in subfolders')
    parser.add_argument('--interactive', action='store', help='interactive mode', default=False)

    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':

    params = process_arguments(sys.argv[1:])
    markov_texts_path = params['markov_texts_path']
    keras_lstm_models_path = params['keras_models_path']
    word_lstm_models_path = params['word_lstm_models_path']

    generator = Generator()
    generator.init_markov(text_files_path=markov_texts_path, max_models=40)
    generator.init_word_level_lstm(models_path=word_lstm_models_path, max_models=40)
    generator.init_keras_lstm(models_path=keras_lstm_models_path, max_models=40)

    interactive = params['interactive']
    if not interactive:
        interactive = settings.INTERACTIVE

    if settings.START_WEBSERVER:
        webserver.server.set_generator(generator)
        webserver.server.launch()

    spell_checker = postpreprocess.spell_check.PreProcessor()

    while interactive:
        try:
            input = raw_input('input: ')

            if input == 'exit':
                break
            # 1. preprocess
            input_checked, input_spellchecked, input_grammarchecked = spell_checker.process(input, return_to_lower=True)

            # 2. apply technique
            result = ''
            # generator.mode = generator.WORD_RNN
            if generator.mode is generator.MARKOV:
                result = generator.print_markov_result(input=input_checked)
            if generator.mode is generator.KERAS_LSTM:
                result = generator.print_keras_lstm_result(input=input_checked)
            if generator.mode is generator.WORD_RNN:
                result = generator.print_word_rnn_result(input=input_checked)

            # temp hack- works only for word_level_rnn
            if result == 'no answer':
                print('WORDRNN: no answer')
                result = generator.get_random_answer()

            # 3. postprocess
            output_checked, _, __ = spell_checker.process(result, return_to_lower=False)
            print('--- Final Result ---')
            print(output_checked)
        except:
            print('Error')
