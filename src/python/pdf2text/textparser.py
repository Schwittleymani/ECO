from pattern.en import parse, Text

class ParseStatistic(object):
    all_sentences = 0
    proper_sentences = 0
    files_parsed = 0

    too_few_words = 0
    first_word_is_number = 0
    sentence_contains_brackets = 0
    sentence_contains_number = 0
    sentence_too_many_comma = 0

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

    def parse(self, text):
        self.proper_sentences = []
        text = Text(parse(text,
                          tokenize=True,
                          tags=True,
                          chunks=True,
                          relations=False,
                          lemmata=False,
                          encoding='utf-8',
                          tagset=None))

        self.statistic.all_sentences += len(text)
        self.statistic.files_parsed += 1
        for sentence in text:
            if len(sentence.words) > self.MIN_WORD_COUNT:
                first_word = sentence.words[0]
                first_word_tag = first_word.type
                if first_word_tag != "CD":
                    if not self.contains_tag(sentence, "(") \
                            and not self.contains_tag(sentence, ")") \
                            and not self.contains_tag(sentence, "\""):
                        if self.get_count_tag(sentence, "CD") < 1:
                            if self.get_count_tag(sentence, ",") < 3:
                                self.proper_sentences.append(sentence)
                            else:
                                # the sentence has more than 2 occurrences of a comma(,)
                                self.statistic.sentence_too_many_comma += 1
                        else:
                            # the sentence contains a number
                            self.statistic.sentence_contains_number += 1
                    else:
                        # the sentence contains either ( ) or \
                        self.statistic.sentence_contains_brackets += 1
                else:
                    # first word of the sentence is a number
                    self.statistic.first_word_is_number += 1
            else:
                # too few words in the sentence
                # removes sentences like these: https://gist.github.com/mrzl/32b9763bd943c18cb77cd1167a87640a
                self.statistic.too_few_words += 1
        self.statistic.proper_sentences += len(self.proper_sentences)
        print('Parsed ' + str(len(self.proper_sentences)) + ' proper sentences.')
