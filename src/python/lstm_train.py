from lstm_wrapper import LSTMWrapper
import sys
import argparse


def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    # training parameters
    parser.add_argument('--input', action='store', help='the path to the input text file')
    parser.add_argument('--iterations', action='store', help='how many iterations to train')
    parser.add_argument('--epochs', action='store', help='how many epochs to train')
    parser.add_argument('--steps', action='store', help='how many steps. aka i dont really know what it does, yet')
    parser.add_argument('--model_save_path', action='store', help='path to save the exported models to')
    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input_text_path = params['input']
    iterations = int(params['iterations'])
    epochs = int(params['epochs'])
    steps = int(params['steps'])
    model_save_path = params['model_save_path']

    print('Running LSTM with parameters:')
    print('training input file: ' + input_text_path)
    print('training iterations: ' + str(iterations))
    print('training epochs: ' + str(epochs))
    print('training steps: ' + str(steps))

    maxlen = 100

    lstm = LSTMWrapper(maxlen=maxlen, step=steps)
    lstm.load(path=input_text_path)
    lstm.train(iterations=iterations, epochs=epochs)

    lstm.save_model(save_path=model_save_path)