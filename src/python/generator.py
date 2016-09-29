import markov.markov2_wrapper
import keras_lstm.lstm_wrapper
import word_level_rnn.word_lstm_wrapper 

class Generator(object):
    def __init__(self):
        self.markov = None
        self.lstm = None

        self.MARKOV = 0
        self.KERAS_LSTM = 1
        self.WORD_RNN = 2

        self.mode = self.KERAS_LSTM

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
        markov_author, markov_result = generator.sample_markov(input=input)
        #print('Markov Chain input: \"' + input + '\" - author: ' + markov_author)

        result = markov_result.strip()
        #print(result)

        return result

    def print_keras_lstm_result(self, input):
        keras_lstm_author, keras_lstm_result = generator.sample_keras_lstm(input=input)
        #print('Keras LSTM input: \"' + input + '\" - author: ' + keras_lstm_author)

        result = keras_lstm_result.strip()
        #print(result)

        return result

    def print_word_rnn_result(self, input):
        word_level_lstm_author, word_level_lstm_result = generator.sample_word_level_lstm(input=input, output_length=10)
        #print('Word level LSTM input: \"' + input + '\" - author: ' + word_level_lstm_author)
        #print(word_level_lstm_result)

        return word_level_lstm_result

    def print_result(input):
        result = ''
        if self.mode is MARKOV:
            result = self.print_markov_result(input=input_checked)
        if self.mode is KERAS_LSTM:
            result = self.print_keras_lstm_result(input=input_checked)
        if self.mode is WORD_RNN:
            result = self.print_word_rnn_result(input=input_checked)   
        if result == 'no answer':
            result = get_random_answer()  
        return result      