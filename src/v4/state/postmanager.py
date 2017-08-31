import base64
from enum import Enum
import json
from PIL import Image
import random

from misc.kaomoji import KaomojiHelp
from state.reddit.generator import Generator
from state.reddit.pandasdata import PandasData
from state.reddit.pandasfilter import PandasFilter


class PostType(Enum):
    POST_TYPE_KAOMOJI = 0
    POST_TYPE_GIF = 1
    POST_TYPE_REDDIT = 2
    #POST_TYPE_START = -1
    #POST_TYPE_USER = 0
    #POST_TYPE_HANDWRITING = 2
    #POST_TYPE_RNN_NAILS = 3
    #POST_TYPE_NAILS_CITATION = 5


class Post(object):
    def __init__(self, previous):
        self.previousPost = previous
        print("new post: " + str(self))

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

    def dict(self):
        """
        returns a dict of the post
        """
        raise NotImplementedError("Should have implemented this")


class StartPost(Post):
    def __init__(self, previous, text=""):
        super().__init__(previous)
        self._text = text

    def text(self):
        return self._text

    def json(self):
        pass

    def dict(self):
        pass


kao = KaomojiHelp()


class KaomojiPost(Post):
    def __init__(self, previous):
        super().__init__(previous)
        # todo: check the previous text representation
        # todo: for correlation with available kaomojis
        self.kaomoji = kao.get(random.randint(0, kao.len() - 1))

    def text(self):
        return self.kaomoji.rawText()

    def dict(self):
        dict = {}
        dict['textRepresentation'] = self.text()
        dict['text'] = self.kaomoji.kaomojiText()
        dict['postType'] = "KAOMOJI_POST"
        dict['renderType'] = "PLAIN"
        dict['image'] = None
        return dict

    def json(self):
        dump = json.dumps(self.dict())
        return dump


class GifPost(Post):
    def __init__(self, previous):
        super().__init__(previous)
        self.path = 'data/gif/1469571231514.gif'
        with open(self.path, "rb") as image_file:
            self.encoded_string = base64.b64encode(image_file.read())
        self.gif = Image.open(self.path)

    def text(self):
        return self.previousPost.text()

    def dict(self):
        dict = {}
        dict['textRepresentation'] = self.path
        dict['text'] = self.text()
        dict['postType'] = "GIF_POST"
        dict['renderType'] = "GIF"
        dict['image'] = str(self.encoded_string)
        return dict

    def json(self):
        dump = json.dumps(self.dict())
        return dump


feather_file = 'data/reddit/test_reddit_4chan.feather'
block_words = open('data/reddit/blocked_words.txt').readlines()
block_chars = "".join(open('data/reddit/blocked_chars.txt').readlines())
data = PandasData(feather_file, block_words=block_words)
data.load()
df = data.df
generator = Generator(PandasFilter(df), block_words=block_words, block_chars=block_chars)


class RedditPost(Post):
    def __init__(self, previous):
        super().__init__(previous)

        generator.reset()
        generator.clear()
        generator.length(50, 150).shannon_entropy(1.0, 10)
        generator.generate()
        self._text = generator.sentences()[0].text

    def text(self):
        return self._text

    def dict(self):
        dict = {}
        dict['textRepresentation'] = self.text()
        dict['text'] = "reddit/4chan"
        dict['postType'] = "REDDIT_POST"
        dict['renderType'] = "PLAIN"
        dict['image'] = None
        return dict

    def json(self):
        dump = json.dumps(self.dict())
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

    def add(self):
        randomType = random.choice(list(PostType))
        new = self.get(randomType, self.last())
        self.posts.append(new)

    @staticmethod
    def get(ptype, previous):
        if ptype is PostType.POST_TYPE_KAOMOJI:
            return KaomojiPost(previous=previous)
        if ptype is PostType.POST_TYPE_GIF:
            return GifPost(previous=previous)
        if ptype is PostType.POST_TYPE_REDDIT:
            return RedditPost(previous=previous)