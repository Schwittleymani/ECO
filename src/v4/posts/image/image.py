import json
import os
import random
import operator
from PIL import Image


class AsciiHelper(object):
    ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

    def image2ascii(self, image, new_width=180):
        if image:
            image = self._scale_image(image)
            image = self._convert_to_grayscale(image)

            pixels_to_chars = self._map_pixels_to_ascii_chars(image)
            len_pixels_to_chars = len(pixels_to_chars)

            image_ascii = [pixels_to_chars[index: index + new_width] for index in
                           range(0, len_pixels_to_chars, new_width)]

            return "\n".join(image_ascii)
        else:
            return False

    def _scale_image(self, image, new_width=180):
        """
        Resizes an image preserving the aspect ratio.
        """
        (original_width, original_height) = image.size
        aspect_ratio = original_height / float(original_width)
        new_height = int(aspect_ratio * new_width)

        new_image = image.resize((new_width, int(new_height/2)))
        return new_image

    def _convert_to_grayscale(self, image):
        return image.convert('L')

    def _map_pixels_to_ascii_chars(self, image, range_width=25):
        """
        Maps each pixel to an ascii char based on the range
        in which it lies.

        0-255 is divided into 11 ranges of 25 pixels each.
        """

        pixels_in_image = list(image.getdata())
        pixels_to_chars = []
        for pixel_value in pixels_in_image:
            pixels_to_chars.append(self.ASCII_CHARS[int(pixel_value / range_width)])

        return "".join(pixels_to_chars)

    @staticmethod
    def load(image_path):
        image = None
        try:
            image = Image.open(image_path)
        except Exception as e:
            print("Unable to open image file {image_filepath}.".format(image_filepath=image_path))
            print(e)

        return image


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

    helper = AsciiHelper()
    ascii = helper.image2ascii(helper.load('server/static/image/gif.gif'))
    print(ascii)
