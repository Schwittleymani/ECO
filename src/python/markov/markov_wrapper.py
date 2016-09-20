import markovify


class MarkovWrapper(object):
    def __init__(self):
        self.text = None
        self.text_model = None

    def train(self, input_path, state_size):
        with open(input_path, 'r') as file:
            self.text = file.read()

        self.text_model = markovify.Text(self.text, state_size=state_size)

    def sample_short(self, length):
        return self.text_model.make_short_sentence(char_limit=length, tries=100)

    def sample(self, prime, length):
        return self.text_model.make_sentence_with_start(beginning=prime, tries=10)