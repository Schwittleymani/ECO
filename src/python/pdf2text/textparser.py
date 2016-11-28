from pattern.en import parse, Text

class ParseStatistic(object):
    properties = {}
    properties['all_sentences'] = 0
    properties['proper_sentences'] = 0
    properties['too_few_words'] = 0
    properties['first_word_is_number'] = 0
    properties['sentence_contains_brackets'] = 0
    properties['sentence_contains_number'] = 0
    properties['sentence_too_many_comma'] = 0
    properties['too_many_short_words'] = 0

class TextParser(object):
    """
    This parses a massive string, that contains an entire book. Splits
    it into sentences and either discards the sentence if the pdf->txt
    conversion was faulty already or returns it.

    This is using pattern.en as a analysis library http://www.clips.ua.ac.be/pages/pattern-en#parser
    The tags of words are being analyzed: http://www.clips.ua.ac.be/pages/mbsp-tags
    """
    def __init__(self):
        self.proper_sentences = []
        self.MIN_WORD_COUNT = 10
        self.statistic = ParseStatistic()

    @staticmethod
    def get_count_tag(sentence, tag):
        count = 0
        for word in sentence:
            if word.type == tag:
                count += 1
        return count

    @staticmethod
    def contains_tag(sentence, tag):
        for word in sentence:
            if word.type == tag:
                return True

        return False

    @staticmethod
    def get_perc_single_char_words(sentence):
        short_word = 0
        long_word = 0
        for word in sentence:
            if len(word.string) < 2:
                short_word += 1
            else:
                long_word += 1
        perc = float(short_word) / float(short_word + long_word)
        return perc

    def parse(self, text):
        self.proper_sentences = []

        self.statistic.properties['all_sentences'] = 0
        self.statistic.properties['proper_sentences'] = 0
        self.statistic.properties['too_few_words'] = 0
        self.statistic.properties['first_word_is_number'] = 0
        self.statistic.properties['sentence_contains_brackets'] = 0
        self.statistic.properties['sentence_contains_number'] = 0
        self.statistic.properties['sentence_too_many_comma'] = 0
        self.statistic.properties['too_many_short_words'] = 0

        text = Text(parse(text,
                          tokenize=True,
                          tags=True,
                          chunks=True,
                          relations=False,
                          lemmata=False,
                          encoding='utf-8',
                          tagset=None))

        self.statistic.properties['all_sentences'] += len(text)
        for sentence in text:
            if len(sentence.words) > self.MIN_WORD_COUNT:
                first_word = sentence.words[0]
                first_word_tag = first_word.type
                if self.get_perc_single_char_words(sentence) < 0.5:
                    if first_word_tag != "CD":
                        if not self.contains_tag(sentence, "(") \
                                and not self.contains_tag(sentence, ")") \
                                and not self.contains_tag(sentence, "\""):
                            if self.get_count_tag(sentence, "CD") < 1:
                                if self.get_count_tag(sentence, ",") < 3:
                                    self.proper_sentences.append(sentence)
                                else:
                                    # the sentence has more than 2 occurrences of a comma(,)
                                    self.statistic.properties['sentence_too_many_comma'] += 1
                            else:
                                # the sentence contains a number
                                self.statistic.properties['sentence_contains_number'] += 1
                        else:
                            # the sentence contains either ( ) or \
                            self.statistic.properties['sentence_contains_brackets'] += 1
                    else:
                        # first word of the sentence is a number
                        self.statistic.properties['first_word_is_number'] += 1
                else:
                    # too many short words
                    self.statistic.properties['too_many_short_words'] += 1
            else:
                # too few words in the sentence
                # removes sentences like these: https://gist.github.com/mrzl/32b9763bd943c18cb77cd1167a87640a
                self.statistic.properties['too_few_words'] += 1
        self.statistic.properties['proper_sentences'] += len(self.proper_sentences)
        print('Parsed ' + str(len(self.proper_sentences)) + ' proper sentences.')
