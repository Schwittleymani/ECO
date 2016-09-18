from lstm_wrapper import LSTMWrapper
import sys
import argparse


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # sampling parameters
    parser.add_argument('--model_load_path', action='store', help='path to save the exported models to')
    parser.add_argument('--diversity', action='store', help='how experimental is the output')
    parser.add_argument('--output_length', action='store', help='how many characters to sample')
    params = vars(parser.parse_args(args))

    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    model_path = params['model_load_path']
    diversity = float(params['diversity'])
    output_length = int(params['output_length'])

    print('sample diversity: ' + str(diversity))
    print('sample output character length: ' + str(output_length))

    maxlen = 100

    lstm = LSTMWrapper(maxlen=maxlen, step=3)
    lstm.load_model(model_path)

    while True:
       input = raw_input('input: ')
       output = lstm.sample(diversity=diversity, seed=input.rjust(maxlen), output_length=output_length)
       output = output[maxlen - len(input):]
       print(output)