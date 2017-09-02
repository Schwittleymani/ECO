import re
import os
import json
import random


class Kaomoji(object):
    def __init__(self, kaomoji, emotions):
        self._raw = kaomoji
        self._emotions = emotions

    def kaomoji(self):
        return self._raw

    def emotions(self):
        return self._emotions


class KaomojiHelp(object):
    def __init__(self):
        self.kaomoji_json = json.loads(open("data/kaomoji.json", 'r').read())
        self.dictionary = {}
        index = 0
        for i in self.kaomoji_json:
            keywords = self.kaomoji_json[i]['keywords']
            keywords.append(i)
            self.dictionary[index] = (keywords, self.kaomoji_json[i]['icon'])
            index += 1

    def random(self):
        key, value = random.choice(list(self.dictionary.items()))
        return Kaomoji(value[1], value[0])

    def find(self, words):
        found_matches = []
        for word in words:
            for key, value in self.dictionary.items():
                if word.lower() in value[0]:
                    found_matches.append(Kaomoji(value[1], value[0]))

        # if empty, no found match
        if not found_matches:
            return None

        return random.choice(found_matches)


if __name__ == '__main__':
    kao = KaomojiHelp2()
    print(kao.random().kaomoji())
