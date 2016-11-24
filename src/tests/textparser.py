from pattern.en import parse, Text

class TextParser(object):
    def __init__(self):
        self.proper_sentences = []
        self.MIN_WORD_COUNT = 10

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
        text = Text(parse(text,
                          tokenize=True,
                          tags=True,
                          chunks=True,
                          relations=False,
                          lemmata=False,
                          encoding='utf-8',
                          tagset=None))

        index = 0
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
            index += 1

        print('Parsed ' + str(len(self.proper_sentences)) + ' proper sentences.')
