from lstm_wrapper import LSTMWrapper
import sys
import argparse
import os


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--input', action='store', help='the path to the input text file')
    parser.add_argument('--iterations', action='store', help='how many iterations to train')
    parser.add_argument('--epochs', action='store', help='how many epochs to train')
    parser.add_argument('--max_input_length', action='store', help='how many characters can be input. heavily influences training time')
    parser.add_argument('--model_save_path', action='store', help='path to save the exported models to')
    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_text_path = params['input']
    iterations = int(params['iterations'])
    epochs = int(params['epochs'])
    max_input_chars = int(params['max_input_length'])
    model_save_path = params['model_save_path']

    print('Running LSTM with parameters:')
    print('training input file: ' + input_text_path)
    print('training iterations: ' + str(iterations))
    print('training epochs: ' + str(epochs))

    for i in xrange(1, max_input_chars):
        lstm = LSTMWrapper(maxlen=i)
        lstm.load(path=input_text_path)
        lstm.train(iterations=iterations, epochs=epochs)

        output_filename = os.path.splitext(os.path.basename(input_text_path))[0] + '_' + str(i).zfill(2)
        lstm.save_model(save_path=model_save_path, filename=output_filename)