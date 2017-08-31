import operator

from state.reddit.sentence import Sentence


class Generator(object):
    def __init__(self, pf, block_words=None, block_chars=None):
        self._pf = pf
        self._block_words = block_words
        self._block_chars = block_chars

        self._sentences = []

        self.reset()

    def map(self, v, lmi, lma, rmi, rma):
        return rmi + (float(v - lmi) / float(lma - lmi) * (rma - rmi))

    def reset(self):
        self.pf = self._pf
        self._do_filter_length = False
        self._do_filter_occurance = False
        self._do_filter_entropy = False
        self._do_filter_vbe = False
        self._do_filter_w2v_entropy = False
        self._do_filter_special_ratio = False

        self._min_vbe = None
        self._max_vbe = None
        self._min_length = None
        self._max_length = None
        self._min_occurance = None
        self._min_shannon_entropy = None
        self._max_shannon_entropy = None
        self._min_w2v_entropy = None
        self._max_w2v_entropy = None
        self._min_special_ratio = None

    def disable_length(self):
        self._do_filter_length = False

    def disable_occurance(self):
        self._do_filter_occurance = False

    def disable_shannon_entropy(self):
        self._do_filter_entropy = False

    def disable_vbe(self):
        self._do_filter_vbe = False

    def disable_w2v_entropy(self):
        self._do_filter_w2v_entropy = False

    def disable_special_entropy(self):
        self._do_filter_special_ratio = False

    def length(self, min_length, max_length):
        self._do_filter_length = True
        self._min_length = min_length
        self._max_length = max_length
        return self

    def occurance(self, min_occurance=0):
        self._do_filter_occurance = True
        self._min_occurance = min_occurance
        return self

    def shannon_entropy(self, minent=0, maxent=10):
        self._do_filter_entropy = True
        self._min_shannon_entropy = minent
        self._max_shannon_entropy = maxent
        return self

    def vbe(self, min_vbe, max_vbe=2.0):
        self._do_filter_vbe = True
        self._min_vbe = min_vbe
        self._max_vbe = max_vbe
        return self

    def w2v_entropy(self, min_w2v, max_w2v):
        self._do_filter_w2v_entropy = True
        self._min_w2v_entropy = min_w2v
        self._max_w2v_entropy = max_w2v
        return self

    def special_ratio(self, min_special_ratio):
        self._do_filter_special_ratio = True
        self._min_special_ratio = min_special_ratio
        return self

    def has_weird_chars(self, sentence):
        for char in self._block_chars:
            if char in sentence:
                return True

        return False

    def contains_blocked_word(self, sentence):
        for word in self._block_words:
            if word.rstrip().lower() in sentence.lower():
                print("blocking sentence with blocked word: " + sentence)
                return True
        return False

    def generate(self):
        if self._do_filter_length:
            self.pf.filter_length(self._min_length, self._max_length)
        if self._do_filter_occurance:
            self.pf.filter_rel_occurance(self._min_occurance)
        if self._do_filter_entropy:
            self.pf.filter_shannon(self._min_shannon_entropy, self._max_shannon_entropy)
        if self._do_filter_vbe:
            self.pf.filter_vbe(self._min_vbe, self._max_vbe)
        if self._do_filter_w2v_entropy:
            self.pf.filter_w2v_entropy(self._min_w2v_entropy, self._max_w2v_entropy)
        if self._do_filter_special_ratio:
            self.pf.filter_special_ratio(self._min_special_ratio)

        # remove lines breaks and duplicates
        self.pf.finish()

        raw_sentences_only = list(map(operator.attrgetter('text'), self._sentences))

        chosen_subreddit = "NONE"
        if len(self.pf) > 1:
            try_times = 30
            index = 0
            random_sentence = self.pf.random()
            random_string = random_sentence[0]
            chosen_subreddit = random_sentence[1]
            while random_string in raw_sentences_only \
                    or self.has_weird_chars(random_string) \
                    or self.contains_blocked_word(random_string):
                if index > try_times:
                    print("Using this sentence twice: " + random_string)
                    break
                random_sentence = self.pf.random()
                random_string = random_sentence[0]
                chosen_subreddit = random_sentence[1]
                index += 1
        else:
            random_string = "--- NOT ENOUGH OPTIONS ---"

        sentence = Sentence()
        sentence.text = random_string
        sentence.subreddit = chosen_subreddit
        sentence.options = len(self.pf)
        sentence.length = (self._min_length, self._max_length)
        sentence.vbe = (self._min_vbe, self._max_vbe)
        sentence.occurance = self._min_occurance
        sentence.shannon = self._min_shannon_entropy
        sentence.w2v = (self._min_w2v_entropy, self._max_w2v_entropy)
        sentence.special_ratio = self._min_special_ratio

        self._sentences.append(sentence)
        self.pf.reset()

    def sentences(self):
        return self._sentences

    def clear(self):
        self._sentences = []
