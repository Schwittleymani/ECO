from keras.models import Sequential
from keras.models import load_model, model_from_json
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import numpy as np
import pickle
import os


class LSTMWrapper(object):
    def __init__(self, maxlen, step):
        self.maxlen = maxlen
        self.step = step
        self.name = None

    def load(self, path):
        text = open(path).read().lower()
        print('corpus length:', len(text))

        self.chars = sorted(list(set(text)))
        print('total chars:', len(self.chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

        # cut the text in semi-redundant sequences of maxlen characters
        sentences = []
        next_chars = []
        for i in range(0, len(text) - self.maxlen, self.step):
            sentences.append(text[i: i + self.maxlen])
            next_chars.append(text[i + self.maxlen])
        print('nb sequences:', len(sentences))

        print('Vectorization...')
        self.X = np.zeros((len(sentences), self.maxlen, len(self.chars)), dtype=np.bool)
        self.y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                self.X[i, t, self.char_indices[char]] = 1
                self.y[i, self.char_indices[next_chars[i]]] = 1

        # build the model: a single LSTM
        print('Build model...')
        self.model = Sequential()
        self.model.add(LSTM(128, input_shape=(self.maxlen, len(self.chars))))
        self.model.add(Dense(len(self.chars)))
        self.model.add(Activation('softmax'))

        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    def train(self, iterations, epochs, model_save_path=None, save_every=0):
        # train the model
        for iteration in xrange(iterations):
            print('Iteration ' + str(iteration) + ' / ' + str(iterations))
            self.model.fit(self.X, self.y, batch_size=128, nb_epoch=epochs)

            if save_every != 0 and iteration % save_every == 0:
                output_path = model_save_path + '_iteration' + str(iteration)
                self.save_model(output_path)

    def sample(self, diversity, seed, output_length):
        output_text = seed.rjust(self.maxlen)
        input_text = seed.rjust(self.maxlen)
        for i in range(output_length):
            x = np.zeros((1, self.maxlen, len(self.chars)))
            for t, char in enumerate(input_text):
                x[0, t, self.char_indices[char]] = 1.

            preds = self.model.predict(x, verbose=0)[0]
            next_index = self.__sample_character(preds, diversity)
            next_char = self.indices_char[next_index]

            input_text = input_text[1:] + next_char

            output_text += next_char

        return output_text

    def save_model(self, path):
        directory, filename = os.path.split(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        print('Saving model to' + path)

        model_json = self.model.to_json()
        with open(path + '.json', 'w') as json_file:
            json_file.write(model_json)
        self.model.save_weights(path)

        with open(path + '_chars.pkl', 'wb') as file:
            pickle.dump(self.chars, file, pickle.HIGHEST_PROTOCOL)

        with open(path + '_char_indices.pkl', 'wb') as file:
            pickle.dump(self.char_indices, file, pickle.HIGHEST_PROTOCOL)

        with open(path + '_indices_char.pkl', 'wb') as file:
            pickle.dump(self.indices_char, file, pickle.HIGHEST_PROTOCOL)

    def load_model(self, path):
        print('Loading model from  ' + path)

        json_file = open(path + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights(path)

        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)

        with open(path + '_chars.pkl', 'rb') as file:
            self.chars = pickle.load(file)

        with open(path + '_char_indices.pkl', 'rb') as file:
            self.char_indices = pickle.load(file)

        with open(path + '_indices_char.pkl', 'rb') as file:
            self.indices_char = pickle.load(file)

    def __sample_character(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)
