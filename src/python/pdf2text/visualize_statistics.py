import sys
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np


def process_arguments(args):
    parser = argparse.ArgumentParser(description='visualize the statistics')

    parser.add_argument('--statistics_path', action='store', help='path to the file that holds the statistics')
    params = vars(parser.parse_args(args))

    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    path = params['statistics_path']

    lines = open(path, 'r').readlines()
    labels = lines[0].split(';')[1:]

    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1, len(labels)))

    values = [0] * len(labels)

    plt.rcParams['font.size'] = 9.0

    for stat in lines[1:]:
        sizes = list(map(int, stat.split(';')[1:]))
        index = 0
        for v in sizes:
            values[index] += v
            index += 1

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
        return my_autopct
    patches, texts, autotexts = plt.pie(values,              # data
        labels=labels,      # slice labels
        colors=colors,      # array of colours
        pctdistance=0.7,
        autopct=make_autopct(values),  # print the values inside the wedges
        shadow=True,        # enable shadow
        startangle=70       # starting angle
    )

    for text in texts:
        text.set_fontsize(6)
    for text in autotexts:
        text.set_fontsize(6)

    print(sum(values))

    for index, item in enumerate(labels):
        val = ': ' + str(values[index]) + ' ( ' + str(round((values[index] / float(sum(values))) * 100.0, 2)) + ' % )'
        labels[index] += val
    plt.legend(labels, fontsize=5, loc="best")
    plt.axis('equal')

    # getting the filename of the statistics, and saving the statistics image with the same name
    head, tail = os.path.split(path)
    tail = tail.replace('.txt', '.png')
    plt.savefig(tail, dpi=300)