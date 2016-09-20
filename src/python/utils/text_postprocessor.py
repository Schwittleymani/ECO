import sys
import argparse
import re

def process_arguments(args):
    parser = argparse.ArgumentParser(description='using a lstm with text')

    parser.add_argument('--input', action='store', help='txt file to process')
    parser.add_argument('--output', action='store', help='file to save the processed text t o')
    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    input = params['input']
    output = params['output']

    text_file = open(input, 'r')
    text = text_file.read()
    
    text = text.lower()

    removed_chars = []
    removed_chars.append('0')
    removed_chars.append('1')
    removed_chars.append('2')
    removed_chars.append('3')
    removed_chars.append('4')
    removed_chars.append('5')
    removed_chars.append('6')
    removed_chars.append('7')
    removed_chars.append('8')
    removed_chars.append('9')
    removed_chars.append('(')
    removed_chars.append(')')
    removed_chars.append('[')
    removed_chars.append(']')
    removed_chars.append('&')
    removed_chars.append('%')
    removed_chars.append(';')
    removed_chars.append('*')
    removed_chars.append('\n')

    # replace special chars with space
    for char in removed_chars:
        text = text.replace(char, ' ')

    # this part is taken from: https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    #text = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", text)
    text = re.sub(r"\'s", " \'s", text)
    text = re.sub(r"\'ve", " \'ve", text)
    text = re.sub(r"n\'t", " n\'t", text)
    text = re.sub(r"\'re", " \'re", text)
    text = re.sub(r"\'d", " \'d", text)
    text = re.sub(r"\'ll", " \'ll", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\(", " \( ", text)
    text = re.sub(r"\)", " \) ", text)
    text = re.sub(r"\?", " \? ", text)
    text = re.sub(r"\s{2,}", " ", text)

    # remove all doubled spaces
    text = ' '.join(text.split())

    # replacing some character-space combinations properly
    # needs to be done after the other pre-processing
    text = text.replace(' . ', '. ')
    text = text.replace(' , ', ', ')
    text = text.replace(', ,', ', ')

    with open(output, 'w') as output_file:
        output_file.write(text)

    output_file.close()
