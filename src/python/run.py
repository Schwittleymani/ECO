import markov.markov2_wrapper
import keras_lstm.lstm_wrapper
import word_level_rnn.word_lstm_wrapper
import facebook_osc_connect
import postpreprocess.spell_check

import argparse
import sys
import os
import random


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--keras_models_path', action='store', help='the path to the folder that contains all trained keras lstm models')
    parser.add_argument('--markov_texts_path', action='store', help='the path where text files lie in order to train the markov chains')
    parser.add_argument('--word_lstm_models_path', action='store', help='the path where the models are stored in subfolders')

    params = vars(parser.parse_args(args))

    return params


class Generator(object):
    def __init__(self):
        self.markov = None
        self.lstm = None

        self.MARKOV = 0
        self.KERAS_LSTM = 1
        self.WORD_RNN = 2

        self.mode = self.MARKOV

    def init_markov(self, text_files_path, max_models=100):
        self.markovs = []
        loaded_count = 0
        for root, dirs, files in os.walk(text_files_path):
            for f in files:
                if loaded_count < max_models:
                    file_name = os.path.join(root, f)
                    markov_instance = markov.markov2_wrapper.Markov2Wrapper(file_name)
                    markov_instance.name = f[:20]
                    self.markovs.append(markov_instance)
                    loaded_count += 1

    def init_keras_lstm(self, models_path, max_models=100):
        self.lstms = []
        loaded_count = 0
        for root, dirs, files in os.walk(models_path):
            for dir in dirs:
                path = os.path.join(root, dir)
                for _root, _dirs, _files in os.walk(path):
                    for file in _files:
                        if file.endswith('.h5'):
                            if loaded_count < max_models:
                                final_model_path = os.path.join(path, file)
                                lstm = keras_lstm.lstm_wrapper.LSTMWrapper(maxlen=100, step=2)
                                lstm.load_model(final_model_path)
                                lstm.name = dir # setting the name of this lstm instance
                                self.lstms.append(lstm)

                                loaded_count += 1

    def init_word_level_lstm(self, models_path):
        self.word_lstms = []
        for root, dirs, files in os.walk(models_path):
            for dir in dirs:
                path = os.path.join(root, dir)
                word_lstm = word_level_rnn.word_lstm_wrapper.WordLevelLSTM(load_dir=path)
                self.word_lstms.append(word_lstm)

    def sample_markov(self, input, length=50):
        """
        :param input: the input text to continue with the markov chain
        :param length: the length in characters of the returned output
        :return: the answer found via markov chain
        """
        random_markov_index = random.randint(0, len(self.markovs) - 1)
        selected_markov = self.markovs[random_markov_index]
        return selected_markov.name, selected_markov.sample(input_text=input, length=length)

    def sample_keras_lstm(self, input, diversity=0.3, length=150):
        """
        :param input: the input text to continue with the lstm
        :param diversity: [0-1] the riskyness of the answer. 0 -> 1 increases riskyness
        :param length: the length of the output in characters
        :return: the answer found via lstm
        """
        random_lstm_index = random.randint(0, len(self.lstms) - 1)
        selected_lstm = self.lstms[random_lstm_index]
        return selected_lstm.name, selected_lstm.sample(diversity=diversity, seed=input, output_length=length)

    def sample_word_level_lstm(self, input, sample=1, output_length=50):
        random_word_lstm_index = random.randint(0, len(self.word_lstms) - 1)
        selected_word_lstm = self.word_lstms[random_word_lstm_index]
        return 'NO AUTHOR YET', selected_word_lstm.sample(input=input, sample=sample, output_length=output_length)

    def print_markov_result(self, input):
        markov_author, markov_result = self.sample_markov(input=input)
        #print('Markov Chain input: \"' + input + '\" - author: ' + markov_author)

        result = markov_result.strip()
        #print(result)

        return result

    def print_keras_lstm_result(self, input):
        keras_lstm_author, keras_lstm_result = self.sample_keras_lstm(input=input)
        print('Keras LSTM input: \"' + input + '\" - author: ' + keras_lstm_author)

        result = keras_lstm_result.strip()
        print(result)

        return result

    def print_word_rnn_result(self, input):
        word_level_lstm_author, word_level_lstm_result = self.sample_word_level_lstm(input=input, output_length=10)
        #print('Word level LSTM input: \"' + input + '\" - author: ' + word_level_lstm_author)
        #print(word_level_lstm_result)

        return word_level_lstm_result


def get_random_answer():
    file = open('pre_defined_answers.txt', 'r')
    lines = []
    for line in file.readlines():
        lines.append(line.rstrip())

    return lines[random.randint(0, len(lines) - 1)]


class Main(object):
    def __init__(self, params):

        self.spell_checker = postpreprocess.spell_check.PreProcessor()

        markov_texts_path = params['markov_texts_path']
        keras_lstm_models_path = params['keras_models_path']
        word_lstm_models_path = params['word_lstm_models_path']

        self.generator = Generator()
        self.generator.init_markov(text_files_path=markov_texts_path, max_models=20)

        #self.generator.init_word_level_lstm(models_path=word_lstm_models_path)
        self.generator.init_keras_lstm(models_path=keras_lstm_models_path, max_models=20)

        self.facebook = facebook_osc_connect.OscFacebook()
        self.facebook.add_callback('/get', self.process_from_facebook)

        self.queue = []
        self.threadids = []

    def process(self, input):
        # 1. preprocess
        input_checked, input_spellchecked, input_grammarchecked = self.spell_checker.process(input,
                                                                                             return_to_lower=True)
        print('done pre-checking')
        # 2. apply technique
        result = ''
        self.generator.mode = self.generator.KERAS_LSTM
        if self.generator.mode is self.generator.MARKOV:
            result = self.generator.print_markov_result(input=input_checked)
        if self.generator.mode is self.generator.KERAS_LSTM:
            result = self.generator.print_keras_lstm_result(input=input_checked)
        if self.generator.mode is self.generator.WORD_RNN:
            result = self.generator.print_word_rnn_result(input=input_checked)

        # temp hack- works only for word_level_rnn
        if result == 'no answer':
            result = get_random_answer()

        # 3. postprocess
        output_checked, _, __ = self.spell_checker.process(result, return_to_lower=False)
        print('--- Final Result ---')
        print(output_checked)
        return output_checked

    def process_from_facebook(self, addr, tags, stuff, source):
        print(addr, tags, stuff)
        raw_input = stuff[0]
        thread_id = stuff[1]
        print('raw: ' + raw_input)
        self.threadids.append(thread_id)
        self.queue.append(raw_input)
        #print('thread: ' + thread_id)
        #answer = self.process(input=raw_input)
        #self.facebook.send(answer, threadid=thread_id)

if __name__ == '__main__':

    params = process_arguments(sys.argv[1:])

    main = Main(params=params)

    while True:
        if len(main.queue) > 0:
            try:
                input = main.queue[0]
                threadid = main.threadids[0]
                main.threadids.remove(threadid)
                main.queue.remove(input)
                answer = main.process(input=input)
                main.facebook.send(answer, threadid)
            except:
                print('Error')
        #else:
        #    try:
        #        input = raw_input('input: ')
        #        answer = main.process(input=input)
        #    except:
        #        print('Error')