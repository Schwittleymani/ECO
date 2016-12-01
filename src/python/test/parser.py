import sys

sys.path.insert(0, '../pdf2text/')
import textparser

class ParserTest(object):
    def test_invalid(self):
        lines = open('invalid_lines.txt', 'r').readlines()
        invalid_sentences = '\n'.join(lines)
        parser = textparser.TextParser()
        parser.parse(invalid_sentences)

        if not len(lines) == len(parser.faulty_sentences):
            print('-------------------------')
            print('These lines should be invalid:')
            for line in parser.valid_sentences:
                pass
                print(line.string)
            print('-------------------------')

    def test_valid(self):
        lines = open('valid_lines.txt', 'r').readlines()
        valid_sentences = '\n'.join(lines)
        parser = textparser.TextParser()
        parser.parse(valid_sentences)
        if not len(lines) == len(parser.valid_sentences):
            print('-------------------------')
            print('These lines should be valid:')
            for line in parser.faulty_sentences:
                print(line.string)
            print('-------------------------')

if __name__ == '__main__':
    test = ParserTest()
    test.test_invalid()
    test.test_valid()