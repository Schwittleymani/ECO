import sys
import argparse
import matplotlib.pyplot as plt


def process_arguments(args):
    parser = argparse.ArgumentParser(description='visualize the statistics')

    parser.add_argument('--statistics_path', action='store', help='path to the file that holds the statistics')
    params = vars(parser.parse_args(args))

    return params

if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    path = params['statistics_path']

    lines = open(path, 'r').readlines()
    labels = lines[0].split(',')[1:]

    colors = ['yellowgreen', 'mediumpurple', 'lightskyblue', 'lightcoral', 'darkred', 'blue', 'green']

    remove_index_from_list = labels.index('all_sentences')
    labels.remove('all_sentences')

    values = [0, 0, 0, 0, 0, 0, 0]

    for stat in lines[1:]:
        sizes = list(map(int, stat.split(',')[1:]))
        sizes.pop(remove_index_from_list)
        index = 0
        for v in sizes:
            values[index] += v
            index += 1

    explode = (0, 0, 0, 0, 0, 0, 0)    # proportion with which to offset each wedge

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
        return my_autopct
    plt.pie(values,              # data
        explode=explode,    # offset parameters
        labels=labels,      # slice labels
        colors=colors,      # array of colours
        autopct=make_autopct(values),  # print the values inside the wedges
        shadow=True,        # enable shadow
        startangle=70       # starting angle
    )

    plt.axis('equal')
    plt.show()