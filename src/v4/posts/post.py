import json
import time
import datetime
import gensim
import os
import random
import socket
import giphypop
import requests
import grammar_check
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


class StaticHelper(object):
    def __init__(self):
        # some heavy, static variables

        self._grammar_checker = grammar_check.LanguageTool('en-GB')

        self._kao = KaomojiHelp()
        self._image_helper = ImageHelper(path=data_access.get_model_folder() + '4chan_non_porn_classified.json')
        self._ascii_helper = AsciiHelper()
        self._deep_moji = DeepMojiWrapper()
        self._markov_manager = MarkovManager()
        self._doc2vecSimilarity_manager = Doc2VecSimilarityManager()
        self._giphy = giphypop.Giphy()

        feather_file = data_access.get_model_folder() + '/test_reddit_4chan.feather'
        # WHY SOME REDDIT CRAP IN THE ABSTRACT CLASS?
        print('Loading ' + feather_file + ' for RedditPost')
        block_words = open(data_access.get_data_folder() + 'v4/reddit/blocked_words.txt').readlines()
        block_chars = "".join(open(data_access.get_data_folder() + 'v4/reddit/blocked_chars.txt').readlines())
        data = PandasData(feather_file, block_words=block_words)
        data.load()
        df = data.df

        self._generator = Generator(PandasFilter(df), block_words=block_words, block_chars=block_chars)

        w2v_path = 'word2vec_models/wiki_plus_v3_valid_combined.txt_numpy.w2vmodel'
        print('Loading w2v model: ' + w2v_path)
        model = gensim.models.Word2Vec.load(data_access.get_model_folder() + w2v_path)
        self._nails_finder = NailsSimilarityFinder(model)

    def fix_grammar(self, text):
        matches = self._grammar_checker.check(text)
        fixed = grammar_check.correct(text, matches)

        print('fixed grammar from ' + text + ' to ' + fixed)

        return fixed

    def kaomoji(self):
        return self._kao

    def image(self):
        return self._image_helper

    def ascii(self):
        return self._ascii_helper

    def pandas(self):
        return self._generator

    def deepmoji(self):
        return self._deep_moji

    def nails(self):
        return self._nails_finder

    def markov(self):
        return self._markov_manager

    def d2v_sim(self):
        return self._doc2vecSimilarity_manager

    def giphy(self):
        return self._giphy


helper = StaticHelper()


class Post(object):
    def __init__(self, previous, posttype, text='', user='admin'):
        self._text = text
        self._user = user
        self._type = posttype
        self._attachment = None
        self._style = 'unformatted'
        self._timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        if previous is not None:
            print(previous.type() + ' -> ' + self.type())

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

    def type(self):
        return self._type

    def msg_dict(self):
        """
        returns a dict of the post
        """
        return {
            'user': self._user,
            'text': self._text,
            'attachment': self._attachment,
            'style': self._style,
            'timestamp': self._timestamp,
            'type': self._type
        }


class StartPost(Post):
    """
    this post is just there for the initial post
    because all new posts require a previous post
    this is a way to define the starting topic
    """

    def __init__(self, posttype):
        super().__init__(None, posttype, text='welcome', user='eco')

    def connection(self, previous=None):
        pass


class KaomojiPost(Post):
    def connection(self, previous):
        words = previous.text().split()
        self.kaomoji = helper.kaomoji().find(words)
        if not self.kaomoji:
            self.kaomoji = helper.kaomoji().random()
        self._style = "unformatted"
        self._text = str(self.kaomoji.kaomoji())
        self._user = ' '.join(self.kaomoji.emotions())


class ImagePost(Post):
    def connection(self, previous):
        self._text = previous.text()

        if socket.gethostname() == 'lyrik':
            self.path = helper.image().find(self._text.split())
            self.path = os.path.join('static/image/', self.path)
            print(self.path)
        else:
            self.path = 'static/image/gif.gif'

        self._style = "unformatted"
        self._user = '4chan'
        self._attachment = self.path

        self._ascii = False# bool(random.getrandbits(1))

        if self._ascii:
            self._attachment = None
            self._text = helper.ascii().image2ascii(helper.ascii().load('server/' + self.path))
            self._style = "formatted"
            if self._text is False:
                self._attachment = self.path
                self._style = "unformatted"
                self._text = "imagefuck"


class RedditPost(Post):
    def connection(self, previous):
        helper.pandas().reset()
        helper.pandas().clear()
        helper.pandas().length(30, 200).shannon_entropy(0.0, 10)
        helper.pandas().generate()
        t = helper.pandas().sentences()[0].text
        emoji = helper.deepmoji().predict(t)
        self._text = helper.fix_grammar(t) + ' ' + emoji[0]
        self._user = 'reddit'
        self._style = 'spritz'


class NailsPost(Post):
    def connection(self, previous):
        author, sentence, options = helper.nails().get_similar(previous.text())
        emoji = helper.deepmoji().predict(author)[0]

        self._text = sentence + emoji
        self._user = author + ' options: ' + str(options)
        self._style = 'scroll'


class MarkovPost(Post):
    def connection(self, previous):
        start = ''
        if len(previous.text().split()) > 3:
            start = ' '.join(previous.text().split()[:3])

        author, text = helper.markov().generate_random(start_string=start, len=30)
        self._text = helper.fix_grammar(text)
        self._user = author + ' ~MARKOV'
        self._style = 'emojify;scroll'


class Doc2VecSimilarityPost(Post):
    def connection(self, previous):
        if previous.text() == "":
            text = 'computer cyber space'
        else:
            text = previous.text()

        sentence, author = helper.d2v_sim().get_random_similar(text)
        self._text = sentence
        self._user = author + ' ~D2V'
        self._style = 'spritz'


class AsciiPost(Post):
    def connection(self, previous):
        self.butterfly = open('data/ascii/butterfly.txt', 'r').readlines()
        self._text = ""
        for line in self.butterfly:
            self._text += line
        self._user = 'ascii'
        self._style = 'formatted'


class EmojiPost(Post):
    def connection(self, previous):
        if previous.text() == "":
            emojis = helper.deepmoji().random(count=25)
        else:
            emojis = helper.deepmoji().predict(previous.text())
        self._text = ''

        amount = random.randint(1, 30)
        for i in range(amount):
            for emoji in emojis:
                self._text += emoji

        self._user = 'emo mojo'
        self._style = 'emojify;unformatted'


class GifPost(Post):
    def download_gif(self, keywords, url):
        filename = keywords[:30] + '.gif'
        path = data_access.get_model_folder() + 'gifs/' + filename
        print('saving to ' + path)
        file = open(path, 'wb')
        file.write(requests.get(url).content)
        return filename

    def connection(self, previous):
        try:
            result = [x for x in helper.giphy().search(previous.text())]
            filename = self.download_gif(previous.text(), result[0].media_url)
            path = 'static/image/gifs/' + filename
            print('loading from ' + path)
        except:
            default_search = 'computer cyber space'
            result = [x for x in helper.giphy().search(default_search)]
            filename = self.download_gif(default_search, result[0].media_url)
            path = 'static/image/gifs/' + filename
            print('loading from ' + path)

        self._user = 'giphy'
        self._style = 'formatted'
        self._text = previous.text()
        self._attachment = path


class InteractivePost(Post):
    def connection(self, previous):
        self._user = 'interactive'
        self._style = 'unformatted'
        self._text = ''
