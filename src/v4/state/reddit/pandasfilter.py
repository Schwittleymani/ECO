from enum import Enum
import random
import itertools

class PandasFilter(object):
    ###
    #
    # use like this:
    #
    # data = PandasFilter(df)
    # data.filter_shannon(0.0, 4.0)
    # data.filter_length(1, 40)
    # data.filter_src(PandasFilter.SRC.REDDIT)
    # data.filter_language('en') # interestingly 'No.' is being detected as Portuguese :-/
    # data.filter_occurance(500, 100000000)
    # data.finish()
    # sentences = data.to_list()
    # print(sentences)
    #
    ###

    class SRC(Enum):
        FOUR_CHAN = '4chan'
        REDDIT = 'r'

    def __init__(self, _df):
        self.df = _df
        # saving a second copy for reset()
        self._df = _df

    def filter_shannon(self, min_shannon, max_shannon):
        # filters by shannon entropy
        self.df = self.df[(self.df.s_shannon > min_shannon) & (self.df.s_shannon < max_shannon)]

    def filter_w2v_entropy(self, min_w2v, max_w2v):
        # filters by w2v entropy
        self.df = self.df[(self.df.w2v_avg_distance >= min_w2v) & (self.df.w2v_avg_distance < max_w2v)]

    def filter_vbe(self, min_vbe, max_vbe):
        # filters by VBE (very bad entropy)
        self.df = self.df[(self.df.s_vbe > min_vbe) & (self.df.s_vbe < max_vbe)]

    def filter_length(self, min_length, max_length):
        # filters by character count of sentence
        self.df = self.df[(self.df.s_len > min_length) & (self.df.s_len < max_length)]

    def filter_occurance(self, min_occurance, max_occurance):
        # filters the amount of times the sentence appeared in the entire corpus
        self.df = self.df[(self.df.s_count > min_occurance) & (self.df.s_count < max_occurance)]

    def filter_rel_occurance(self, min_occurance):
        # filters the amount of times the sentence appeared in the entire corpus
        self.df = self.df[(self.df.s_count_rel > min_occurance)]

    def filter_src(self, src):
        # filters by source,- 4chan or reddit
        self.df = self.df[self.df.src.str.contains(src.value)]

    def filter_language(self, lang='en'):
        # filters by language
        self.df = self.df[self.df.s_lang.str.contains(lang)]

    def filter_special_ratio(self, min_special_ratio):
        # filters by ratio of special characters to characters
        self.df = self.df[self.df.s_special_ratio >= min_special_ratio]

    def to_dict(self):
        # returns entire dataframe as json dict
        return self.df.to_dict(orient='records')

    def to_list(self):
        # returns only raw strings as a list
        texts = self.df['s'].tolist()
        return texts

    def to_list_with_subreddits(self):
        # returns raw strings with subreddits as list
        texts = self.df['s'].tolist()
        subreddits = self.df['r_subreddit'].tolist()
        text_subreddit_combination = dict(zip(texts, subreddits))
        return text_subreddit_combination  # texts

    def random(self):
        # returns a random raw string
        index = random.randint(0, len(self.df) - 1)
        try:
            subreddit = self.df.iloc[index]['r_subreddit']
        except:
            subreddit = '4chan'
        return self.df.iloc[index]['s'], subreddit

    def __len__(self):
        # enables len(PandasFilter())
        return len(self.df)

    def finish(self):
        # once we want to access the data, remove duplicates and
        # line breaks only from the previously filtered ones
        self._prune_dupes()
        self._prune_linebreaks()

    def push(self):
        # saves the current dataframe state as reference for later reset()
        self._df = self.df

    def reset(self):
        # resets the PandasFilter to the initial dataframe
        self.df = self._df

    def _prune_dupes(self):
        # removes duplicates from the corpus
        self.df = self.df.drop_duplicates(subset='s')

    def _prune_linebreaks(self):
        # strips all line breaks
        self.df['s'] = self.df['s'].str.replace('\n', '')