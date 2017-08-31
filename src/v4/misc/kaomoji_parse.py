import re
import os


class KaomojiHelp(object):
    def __init__(self, path="data/kaomoji.txt"):
        self.emojis = []
        emoji_lines = open(path, 'r').readlines()
        for line in emoji_lines:
            line = line.rstrip('\n')
            emoji_list = re.split(r'\t+', line.rstrip('\t'))
            self.emojis.append((emoji_list[0], emoji_list[1]))

    def get(self, index):
        return self.emojis[index]

    def len(self):
        return len(self.emojis)


def parse():
    emojis = []

<<<<<<< HEAD
    emoji_files = open("data/kaomoji_files.txt").readlines()
=======
    emoji_files = open("../data/kaomoji_files.txt").readlines()
>>>>>>> af837fc919cb8eb59fe0f5fbc946025341e60ba3
    for file in emoji_files:
        file = file.rstrip('\n')
        path = os.path.join("../data/", file).rstrip('\n')
        emoji_file_lines = open(path).readlines()
        for line in emoji_file_lines:
            line = line.rstrip('\n')
            emoji_list = re.split(r'\t+', line.rstrip('\t'))
            for emoji in emoji_list:
                if emoji is not '':
                    emojis.append((emoji, file))

    print("Found: " + str(len(emojis)) + ' emojis.')

    output = open("../data/kaomoji.txt", 'w')
    for emoji in emojis:
        output.write(emoji[0] + '\t' + emoji[1])
        output.write('\n')

    output.close()


if __name__ == '__main__':
    kao = KaomojiHelp()
    print(kao.get(1))

    # parse the files again, they are already saved in data/kaomoji.txt
    # parse()
