
class Sentence(object):
    def __init__(self):
        self._string = None
        self._subreddit = None
        self._options = None
        self._min_length = None
        self._max_length = None
        self._min_vbe = None
        self._max_vbe = None
        self._min_occ = None
        self._min_shan = None
        self._min_w2v = None
        self._max_w2v = None
        self._special_ratio = None

    @property
    def text(self):
        return self._string

    @text.setter
    def text(self, sen):
        self._string = sen

    @property
    def subreddit(self):
        return self._subreddit

    @subreddit.setter
    def subreddit(self, subreddit):
        self._subreddit = subreddit

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        self._options = options

    @property
    def length(self):
        return 'min_length: ' + str(self._min_length) + ' max_length: ' + str(self._max_length)

    @length.setter
    def length(self, min_max_length):
        self._min_length = min_max_length[0]
        self._max_length = min_max_length[1]

    @property
    def vbe(self):
        return 'min_vbe: ' + str(self._min_vbe) + ' max_vbe: ' + str(self._max_vbe)

    @vbe.setter
    def vbe(self, min_max_vbe):
        self._min_vbe = min_max_vbe[0]
        self._max_vbe = min_max_vbe[1]

    @property
    def occurance(self):
        return 'occurance: ' + str(self._min_occ)

    @occurance.setter
    def occurance(self, min_occurance):
        self._min_occ = min_occurance

    @property
    def shannon(self):
        return 'min_shannon: ' + str(self._min_shan)

    @shannon.setter
    def shannon(self, min_shannon):
        self._min_shan = min_shannon

    @property
    def w2v(self):
        return 'min_w2v: ' + str(self._min_w2v) + ' max_w2v: ' + str(self._max_w2v)

    @w2v.setter
    def w2v(self, min_max_w2v):
        self._min_w2v = min_max_w2v[0]
        self._max_w2v = min_max_w2v[1]

    @property
    def special_ratio(self):
        return 'special_ratio: ' + str(self._special_ratio)

    @special_ratio.setter
    def special_ratio(self, special_ratio):
        self._special_ratio = special_ratio

    def summary(self):
        summary_string = 'subreddit: ' + str(self.subreddit) + ' options: ' + str(
            self.options) + ' ' + self.length + ' ' + self.vbe + ' ' + self.occurance + ' ' + self.shannon + ' ' + self.w2v + ' ' + self.special_ratio
        return summary_string