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

def write_statistics(parser, statistic_filename, output_filename):
    file = open(statistic_filename, 'a')

    file.write(output_filename)

    for key, value in parser.statistic.properties.items():
        file.write(';' + str(value))
    file.write('\n')
    file.close()

def get_last_dir_from_path(path):
    list = path.split('/')
    if path.endswith('/'):
        out = list[-2]
    else:
        out = list[-1]
    return out

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])

    input_path = params['input_path']
    output_path = params['output_path']

    if input_path is None or output_path is None:
        print('Missing parameters.')
        sys.exit(1)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    statistic_filename = get_last_dir_from_path(output_path) + '_statistics.txt'

    parser = textparser.TextParser()
    file = open(statistic_filename, 'a')
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

            output_filename_valid = output_path + filename[:-4]
            output_filename_faulty = output_filename_valid + '_faulty.txt'
            output_filename_valid += '_valid.txt'
            print('Saving to ' + output_filename_valid)
            output_file_valid = open(output_filename_valid, 'w')
            for line in parser.valid_sentences:
                output_file_valid.write(line.string.encode('utf8'))
                output_file_valid.write('\n')

            output_file_faulty = open(output_filename_faulty, 'w')
            for line in parser.faulty_sentences:
                output_file_faulty.write(line.string.encode('utf8'))
                output_file_faulty.write('\n')

            write_statistics(parser, statistic_filename, file_path)

        except TypeError as e:
            print(e)
        except textract.exceptions.ShellError as e:
            print(e)
