import json
import os
import random
import operator


class ImageHelper(object):
    def __init__(self, path):
        self._json = json.loads(open(path, 'r').readlines()[0])

    def random(self):
        return os.path.basename(random.choice(list(self._json.keys())))

    def find(self, words):
        detected = {}
        for key in self._json:
            for category in self._json[key]:
                for word in words:
                    if word.lower() in category[0] and len(word) > 6:
                        detected[os.path.basename(key)] = category[1]

        sorted_detected = sorted(detected.items(), key=operator.itemgetter(1), reverse=True)
        if not sorted_detected:
            return None
        return sorted_detected[0][0]

if __name__ == '__main__':
    image_helper = ImageHelper(path='data/image/ffffound_image_categories.json')
    result = image_helper.find(['scoreboard', 'packet', 'horse', 'pig', 'laptop'])
    print(result)