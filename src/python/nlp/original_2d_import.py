import argparse
import sys
import json
import numpy

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Word2Vec model building')
    parser.add_argument('--json_path', action='store', help='path to the json file')
    params = vars(parser.parse_args(args))
    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    json_path = params['json_path']
    vectors = []
    with open(json_path) as json_file:
        data = json.load(json_file)
        for line in data:
            sentence = line['sentence']
            list = line['point']
            float_list = []
            for int in list:
                number = int / 10000.0
                float_list.append(number)

            vector = numpy.array(float_list)
            vectors.append((sentence, vector))
