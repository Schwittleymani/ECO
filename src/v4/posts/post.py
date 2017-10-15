from enum import Enum
import json
import time
import datetime
import random
import gensim
import os
import socket
from misc import data_access

from posts.reddit.generator import Generator
from posts.reddit.pandasdata import PandasData
from posts.reddit.pandasfilter import PandasFilter

from posts.kaomoji.kaomoji import KaomojiHelp
from posts.image.image import ImageHelper
from posts.image.image import AsciiHelper

from posts.nails.nails import NailsSimilarityFinder

from posts.markov.markov import MarkovManager

from posts.d2vsim.d2vsim import Doc2VecSimilarityManager

from posts.DeepMoji.deepmojiwrapper import DeepMojiWrapper

class Post(object):
    def __init__(self, previous, text='', user='admin'):
        self._text = text
        self._user = user
        self._attachment = None
        self._style = 'unformatted'
        self._timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        self.connection(previous)

    def connection(self, previous):
        """
        makes the connection, generates class variables depending
        on what of the previous post to take into account for
        generating the new post
        """
        raise NotImplementedError("Should have implemented this")

    def json(self):
        """
        convert a post to json in order to send it to the frontend
        """
        return json.dumps(self.msg_dict())

    def text(self):
        return self._text


    # TODO for what?
    def msg_dict(self):
        """
        returns a dict of the post
        """
        return {
            'user': self._user,
            'text': self._text,
            'attachment': self._attachment,
            'style': self._style,
            'timestamp': self._timestamp
        }


class StartPost(Post):
    """
    this post is just there for the initial post
    because all new posts require a previous post

    this is a way to define the starting topic
    """
    def __init__(self):
        super().__init__(None, text='welcome')

    def connection(self, previous=None):
        pass

# some static variable
kao = KaomojiHelp()


class KaomojiPost(Post):
    def __init__(self, previous):
        super().__init__(previous)
        self.kaomoji = kao.random()

    def connection(self, previous):
        words = previous.text().split()
        self.kaomoji = kao.find(words)
        if not self.kaomoji:
            self.kaomoji = kao.random()
        self._text = str(self.kaomoji.kaomoji())
        self._user = self.kaomoji.emotions()


image_helper = ImageHelper(path='data/image/ffffound_image_categories.json')
#image_helper = ImageHelper(path='data/image/test_out_4chan_hc.json')
#image_helper = ImageHelper(path='data/image/test_out_4chan_g.json')
ascii_helper = AsciiHelper()


class ImagePost(Post):
    def __init__(self, previous):
        super().__init__(previous)

    def connection(self, previous):
        self._text = previous.text()

        if socket.gethostname() == 'lyrik':
            image_name = image_helper.find(self._text.split())
            if image_name is None:
                image_name = image_helper.random()

            image_path = os.path.join('static/image/ffffound_scrape/ffffound_images/', image_name)
            #image_path = os.path.join('static/image/4chan_hc/', image_name)
            #image_path = os.path.join('static/image/4chan_g/', image_name)
            self.path = image_path
        else:
            self.path = 'static/image/gif.gif'

        self._user = 'image'
        self._attachment = self.path

        self._ascii = False# bool(random.getrandbits(1))

        if self._ascii:
            self._attachment = None
            self._text = ascii_helper.image2ascii(ascii_helper.load('server/' + self.path))
            self._style = "formatted"
            if self._text is False:
                self._attachment = self.path
                self._style = "unformatted"
                self._text = "imagefuck"


# some heavy, static variables
feather_file = 'data/reddit/test_reddit_4chan.feather'
print('Loading ' + feather_file + ' for RedditPost')
block_words = open('data/reddit/blocked_words.txt').readlines()
block_chars = "".join(open('data/reddit/blocked_chars.txt').readlines())
data = PandasData(feather_file, block_words=block_words)
data.load()
df = data.df
generator = Generator(PandasFilter(df), block_words=block_words, block_chars=block_chars)

deepmoji = DeepMojiWrapper()


class RedditPost(Post):
    def __init__(self, previous):
        """
        uses a class that generates(filters) a new post from reddit/4chan
        this class can be more detailed parametrized. check Generator
        :param previous:
        """
        super().__init__(previous)

    def connection(self, previous):
        generator.reset()
        generator.clear()
        generator.length(30, 200).shannon_entropy(0.0, 10)
        generator.generate()
        t = generator.sentences()[0].text
        emoji = deepmoji.predict(t)
        self._text = t + emoji[0]
        self._user = 'reddit'
        self._style = 'spritz'


w2v_path = 'word2vec_models/wiki_plus_v3_valid_combined.txt_numpy.w2vmodel'
print('Loading w2v model: ' + w2v_path)
model = gensim.models.Word2Vec.load(data_access.get_model_folder() + w2v_path)
nailsFinder = NailsSimilarityFinder(model)


class NailsPost(Post):
    def __init__(self, previous):
        """
        uses a class that generates(filters) a new post from nails corpus
        :param previous:
        """
        super().__init__(previous)

    def connection(self, previous):
        selection = nailsFinder.get_similar(previous.text())
        options = selection[1]
        selected = selection[0]

        emoji = deepmoji.predict(selected['author'])[0]

        self._text = selected['sentence'] + emoji +';'
        self._user = selected['author'] + ' options: ' + str(options)
        self._style = 'scroll'

markovManager = MarkovManager()


class MarkovPost(Post):
    def __init__(self, previous):
        super().__init__(previous)

    def connection(self, previous):
        start = ''
        if len(previous.text().split()) > 3:
            start = ' '.join(previous.text().split()[:3])

        author, text = markovManager.generate_random(start_string=start, len=30)
        self._text = text
        self._user = author + ' ~MARKOV'
        self._style = 'scroll'


doc2vecSimilarityManager = Doc2VecSimilarityManager()


class Doc2VecSimilarityPost(Post):
    def __init__(self, previous):
        super().__init__(previous)

    def connection(self, previous):
        sentence, author = doc2vecSimilarityManager.get_random_similar(previous.text())
        self._text = sentence
        self._user = author + ' ~D2V'
        self._style = 'spritz'


class AsciiPost(Post):
    def __init__(self, previous):
        super().__init__(previous)

    def connection(self, previous):
        self.butterfly = open('data/ascii/butterfly.txt', 'r').readlines()
        self._text = ""
        for line in self.butterfly:
            self._text += line
        self._user = 'ascii'
        self._style = 'formatted'


class EmojiPost(Post):
    def __init__(self, previous):
        super().__init__(previous)

    def connection(self, previous):
        self._text = 'i like :smiley:'
        self._user = "emo"
