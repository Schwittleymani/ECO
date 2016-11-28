import os
import sys
import argparse
import glob

import textract
import textparser


def process_arguments(args):
    parser = argparse.ArgumentParser(description='convert pdfs to text and parse the texts properly')

    parser.add_argument('--input_path', action='store', help='path to folder with pdf files')
    parser.add_argument('--output_path', action='store', help='path to save text files to')
    params = vars(parser.parse_args(args))

    return params

def write_statistics(parser):
    file = open('statistics.txt', 'w')
    file.write('Files parsed: ' + str(parser.statistic.files_parsed)+'\n')
    file.write('All sentences: ' + str(parser.statistic.all_sentences)+'\n')
    file.write('Proper sentences: ' + str(parser.statistic.proper_sentences)+'\n')
    file.write('Too few words: ' + str(parser.statistic.too_few_words)+'\n')
    file.write('First word number: ' + str(parser.statistic.first_word_is_number)+'\n')
    file.write('Contains brackets: ' + str(parser.statistic.sentence_contains_brackets)+'\n')
    file.write('Contains number: ' + str(parser.statistic.sentence_contains_number)+'\n')
    file.write('Too many comma: ' + str(parser.statistic.sentence_too_many_comma)+'\n')
    file.close()


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])

    input_path = params['input_path']
    output_path = params['output_path']

    if input_path is None or output_path is None:
        print('Missing parameters.')
        sys.exit(1)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    parser = textparser.TextParser()
    for file_path in glob.glob(input_path + '/*.pdf'):
        print('Parsing ' + file_path)

        path, filename = os.path.split(file_path)

        try:
            text = textract.process(file_path)
            parser.parse(text.decode('utf-8'))

            output_filename = output_path + filename[:-3]
            output_filename += 'txt'
            output_filename = output_filename.replace(' ', '_')
            output_filename = output_filename.replace('.', '_')
            print('Saving to ' + output_filename)
            output_file = open(output_filename, 'w')
            for line in parser.proper_sentences:
                output_file.write(line.string.encode('utf8'))
                output_file.write('\n')

            write_statistics(parser)

        except TypeError as e:
            print(e)
        except textract.exceptions.ShellError as e:
            print(e)
