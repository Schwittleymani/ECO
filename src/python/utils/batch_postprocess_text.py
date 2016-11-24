import os
import sys
import argparse

import textract
import textparser


def process_arguments(args):
    parser = argparse.ArgumentParser(description='convert pdfs to text and parse the texts properly')

    parser.add_argument('--input_path', action='store', help='path to folder with pdf files')
    parser.add_argument('--output_path', action='store', help='path to save text files to')
    params = vars(parser.parse_args(args))

    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])

    input_path = params['input_path']
    output_path = params['output_path']

    if input_path is None or output_path is None:
        print('Missing parameters.')
        sys.exit(1)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for file in os.listdir(input_path):
        if not file.endswith('.pdf'):
            continue

        print('Parsing ' + input_path + file)

        try:
            text = textract.process(input_path + file)

            parser = textparser.TextParser()
            parser.parse(text.decode('utf-8'))

            output_filename = output_path + file[:-3] + 'txt'
            print('Saving to ' + output_filename)
            output_file = open(output_filename, 'w')
            for line in parser.proper_sentences:
                output_file.write(line.string.encode('utf8'))
                output_file.write('\n')
        except TypeError as e:
            print(e)
        except textract.exceptions.ShellError as e:
            print(e)
