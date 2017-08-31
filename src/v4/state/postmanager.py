import base64
from enum import Enum
import json
from PIL import Image
import random
import time

from misc.kaomoji_parse import KaomojiHelp


class PostType(Enum):
    POST_TYPE_START = -1
    POST_TYPE_USER = 0
    POST_TYPE_KAOMOJI = 1
    POST_TYPE_HANDWRITING = 2
    POST_TYPE_RNN_NAILS = 3
    POST_TYPE_REDDIT = 4
    POST_TYPE_NAILS_CITATION = 5
    POST_TYPE_GIF = 6


class Post(object):
    def __init__(self, previous):
        self.previousPost = previous

    def text(self):
        """
        :return: the text representation of the post
        """
        raise NotImplementedError("Should have implemented this")

    def json(self):
        """
        convert a post to json in order to send it to the frontent
        """
        raise NotImplementedError("Should have implemented this")


class StartPost(Post):
    def __init__(self, previous, text=""):
        super().__init__(previous)
        self._text = text

    def text(self):
        return self._text


class Kaomoji(object):
    def __init__(self, rawText, kaomojiText):
        self._raw = rawText
        self._kaomojiText = kaomojiText

    def rawText(self):
        return self._raw

    def kaomojiText(self):
        return self._kaomojiText

kao = KaomojiHelp()

class KaomojiPost(Post):

    def __init__(self, previous):
        super().__init__(previous)
        # todo: check the previous text representation
        # todo: for correlation with available kaomojis
        k = kao.get(random.randint(0, kao.len()))
        print(k)
        self.kaomoji = Kaomoji(k[0], k[1])

    def text(self):
        return self.kaomoji.rawText()

    def json(self):
        dict = {}
        dict['textRepresentation'] = self.text()
        dict['text'] = self.kaomoji.kaomojiText()
        dict['postType'] = "KAOMOJI_POST"
        dict['renderType'] = "PLAIN"
        dict['image'] = None
        dump = json.dumps(dict)
        return dump


class GifPost(Post):
    def __init__(self, previous):
        super().__init__(previous)
        self.path = 'data/gif/1469571231514.gif'
        with open(self.path, "rb") as image_file:
            self.encoded_string = base64.b64encode(image_file.read())
        self.gif = Image.open(self.path)

    def text(self):
        return self.previousPost.text() + str(time.time())

    def json(self):
        dict = {}
        dict['textRepresentation'] = self.text()
        dict['text'] = self.text()
        dict['postType'] = "GIF_POST"
        dict['renderType'] = "GIF"
        dict['image'] = str(self.encoded_string)
        dump = json.dumps(dict)
        return dump


class PostManager(object):
    def __init__(self):
        self.posts = []
        self.posts.append(StartPost(previous=None, text="Start Text"))

    def last(self):
        return self.posts[-1]

    def add(self, postType):
        new = self.get(postType, self.last())
        self.posts.append(new)
        print(self.posts)

    @staticmethod
    def get(ptype, previous):
        if ptype is PostType.POST_TYPE_KAOMOJI:
            return KaomojiPost(previous=previous)
        if ptype is PostType.POST_TYPE_GIF:
            return GifPost(previous=previous)
