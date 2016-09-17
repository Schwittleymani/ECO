from lstm_wrapper import LSTMWrapper
import sys
import argparse
import os


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # sampling parameters
    parser.add_argument('--model_load_path', action='store', help='path to save the exported models to')
    parser.add_argument('--diversity', action='store', help='how experimental is the output')
    parser.add_argument('--seed', action='store', help='the seed text')
    parser.add_argument('--output_length', action='store', help='how many characters to sample')
    params = vars(parser.parse_args(args))

    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    model_path = params['model_load_path']
    diversity = float(params['diversity'])
    seed_text = params['seed']
    output_length = int(params['output_length'])

    print('sample diversity: ' + str(diversity))
    print('sample seed: ' + seed_text)
    print('sample output character length: ' + str(output_length))

    model_files = []
    for (dirpath, dirnames, filenames) in os.walk(model_path):
        for file in filenames:
            if file.endswith('h5'):
                model_files.append(file)
        #model_files.extend(filenames)
    model_files.sort()

    lstms = []
    maxlen = 1
    for model in model_files:
        lstm = LSTMWrapper(maxlen=maxlen)
        lstm.load_model(model_path, model)
        maxlen += 1
        lstms.append(lstm)

    while True:
       input = raw_input('input: ')
       index = len(input) - 1
       if not index > len(lstms):
           output = lstms[index].sample(diversity=diversity, seed=input, output_length=output_length)
           print('used lstm has maxlen: ' + str(lstms[index].maxlen))
           print(output)