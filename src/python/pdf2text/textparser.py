# -*- coding: utf-8 -*-

from pattern.en import parse, Text
import langdetect


class ParseStatistic(object):
    properties = {}
    properties['valid_sentences'] = 0
    properties['too_few_words'] = 0
    properties['first_word_is_number'] = 0
    properties['sentence_contains_brackets'] = 0
    properties['sentence_contains_number'] = 0
    properties['sentence_too_many_comma'] = 0
    properties['too_many_short_words'] = 0
    properties['sentence_in_german'] = 0
    properties['sentence_in_french'] = 0
    properties['sentence_in_spanish'] = 0
    properties['sentence_in_italian'] = 0
    properties['sentence_in_dutch'] = 0
    properties['sentence_not_english'] = 0
    properties['begins_with_punctuation'] = 0
    properties['weird_chars'] = 0
    properties['first_not_upper'] = 0
    properties['last_not_dot'] = 0
    properties['too_many_dots'] = 0


class TextParser(object):
    """
    This parses a massive string, that contains an entire book. Splits
    it into sentences and either discards the sentence if the pdf->txt
    conversion was faulty already or returns it.

    This is using pattern.en as a analysis library http://www.clips.ua.ac.be/pages/pattern-en#parser
    The tags of words are being analyzed: http://www.clips.ua.ac.be/pages/mbsp-tags
    """

    def __init__(self):
        self.valid_sentences = []
        self.faulty_sentences = []
        self.MIN_WORD_COUNT = 8
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

    @staticmethod
    def get_count_of_special_chars(sentence):
        special_chars = [u'~', u'\\', u'/', u';', u':', u'_', u'·', u'<', u'>', u'<U+', u'�', u'!']
        count = 0
        for char in sentence.string:
            if char in special_chars:
                count += 1
        return count

    def parse(self, text):
        self.valid_sentences = []
        self.faulty_sentences = []

        self.statistic.properties['valid_sentences'] = 0
        self.statistic.properties['too_few_words'] = 0
        self.statistic.properties['first_word_is_number'] = 0
        self.statistic.properties['sentence_contains_brackets'] = 0
        self.statistic.properties['sentence_contains_number'] = 0
        self.statistic.properties['sentence_too_many_comma'] = 0
        self.statistic.properties['too_many_short_words'] = 0
        self.statistic.properties['sentence_in_german'] = 0
        self.statistic.properties['sentence_in_french'] = 0
        self.statistic.properties['sentence_in_spanish'] = 0
        self.statistic.properties['sentence_in_italian'] = 0
        self.statistic.properties['sentence_in_dutch'] = 0
        self.statistic.properties['sentence_not_english'] = 0
        self.statistic.properties['begins_with_punctuation'] = 0
        self.statistic.properties['weird_chars'] = 0
        self.statistic.properties['first_not_upper'] = 0
        self.statistic.properties['last_not_dot'] = 0
        self.statistic.properties['too_many_dots'] = 0

        text = Text(parse(text,
                          tokenize=True,
                          tags=True,
                          chunks=True,
                          relations=False,
                          lemmata=False,
                          encoding='utf-8',
                          tagset=None))

        for sentence in text:
            if len(sentence.words) < self.MIN_WORD_COUNT:
                # too few words in the sentence
                # removes sentences like these: https://gist.github.com/mrzl/32b9763bd943c18cb77cd1167a87640a
                self.statistic.properties['too_few_words'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if self.get_perc_single_char_words(sentence) > 0.5:
                # too many short words
                self.statistic.properties['too_many_short_words'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if sentence.string[0].isdigit():
                # first word of the sentence is a number
                self.statistic.properties['first_word_is_number'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if self.contains_tag(sentence, "(") \
                    or self.contains_tag(sentence, ")"):
                # the sentence contains either ( )
                self.statistic.properties['sentence_contains_brackets'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if self.get_count_tag(sentence, "CD") > 1:
                # the sentence contains a number
                self.statistic.properties['sentence_contains_number'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if self.get_count_tag(sentence, ",") > 2:
                # the sentence has more than 2 occurrences of a comma(,)
                self.statistic.properties['sentence_too_many_comma'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if sentence.string[0] in [u'.', u'\'', u';', u'~', u':', u'-', u'·', u'‘', u'\\']:
                # sentence begins with punctuations
                self.statistic.properties['begins_with_punctuation'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if self.get_count_of_special_chars(sentence) > 1:
                # sentence contains weirdly escaped chars
                self.statistic.properties['weird_chars'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if not sentence.string[0].isupper():
                # first char is not upper case
                self.statistic.properties['first_not_upper'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if not sentence.string[-1] in '.':
                # last char not a dot
                self.statistic.properties['last_not_dot'] += 1
                self.faulty_sentences.append(sentence)
                continue
            if sentence.string.count('.') > 3:
                # too many dots in the sentence
                self.statistic.properties['too_many_dots'] += 1
                self.faulty_sentences.append(sentence)
                continue
            try:
                detected_language = str(langdetect.detect_langs(sentence.string)[0]).split(':')[0]
                if detected_language in 'en':
                    self.valid_sentences.append(sentence)
                    continue
                elif detected_language in 'de':
                    self.statistic.properties['sentence_in_german'] += 1
                    self.faulty_sentences.append(sentence)
                    continue
                elif detected_language in 'fr':
                    self.statistic.properties['sentence_in_french'] += 1
                    self.faulty_sentences.append(sentence)
                    continue
                elif detected_language in 'es':
                    self.statistic.properties['sentence_in_spanish'] += 1
                    self.faulty_sentences.append(sentence)
                    continue
                elif detected_language in 'nl':
                    self.statistic.properties['sentence_in_dutch'] += 1
                    self.faulty_sentences.append(sentence)
                    continue
                elif detected_language in 'it':
                    self.statistic.properties['sentence_in_italian'] += 1
                    self.faulty_sentences.append(sentence)
                    continue
                else:
                    self.statistic.properties['sentence_not_english'] += 1
                    self.faulty_sentences.append(sentence)
                    continue
            except langdetect.lang_detect_exception.LangDetectException:
                self.statistic.properties['sentence_not_english'] += 1
                self.faulty_sentences.append(sentence)
                continue

        self.statistic.properties['valid_sentences'] += len(self.valid_sentences)
        print('Parsed ' + str(len(self.valid_sentences)) + ' proper sentences.')

        sum = 0
        for key, value in self.statistic.properties.iteritems():
            if key not in 'valid_sentences':
                sum += value

        print('Discarded ' + str(sum) + ' invalid sentences.')
