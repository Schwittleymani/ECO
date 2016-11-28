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

def write_statistics(parser, filename):
    file = open('statistics.txt', 'a')

    file.write(filename)

    for key, value in parser.statistic.properties.items():
        file.write(';' + str(value))
    file.write('\n')
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
    file = open('statistics.txt', 'a')
    file.write('filename')
    for key, value in parser.statistic.properties.items():
        file.write(';' + key)
    file.write('\n')
    file.close()

    for file_path in glob.glob(input_path + '/*.pdf'):
        print('Parsing ' + file_path)

        path, filename = os.path.split(file_path)

        try:
            text = textract.process(file_path)

            parser = textparser.TextParser()
            parser.parse(text.decode('utf-8'))

            output_filename = output_path + filename[:-3]
            output_filename += '.txt'
            output_filename = output_filename.replace(' ', '_')
            output_filename = output_filename.replace('.', '_')
            print('Saving to ' + output_filename)
            output_file = open(output_filename, 'w')
            for line in parser.proper_sentences:
                output_file.write(line.string.encode('utf8'))
                output_file.write('\n')

            write_statistics(parser, file_path)

        except TypeError as e:
            print(e)
        except textract.exceptions.ShellError as e:
            print(e)
