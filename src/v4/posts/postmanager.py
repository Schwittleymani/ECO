import random

from posts.post import StartPost
from posts.post import KaomojiPost
from posts.post import ImagePost
from posts.post import RedditPost
from posts.post import EmojiPost
from posts.post import NailsPost
from posts.post import MarkovPost
from posts.post import GifPost
from posts.post import Doc2VecSimilarityPost
from posts.post import InteractivePost

post_types = {
    "POST_TYPE_KAOMOJI": KaomojiPost,
    "POST_TYPE_IMAGE": ImagePost,
    "POST_TYPE_REDDIT": RedditPost,
    "POST_TYPE_EMOJI": EmojiPost,
    "POST_TYPE_NAILS": NailsPost,
    'POST_TYPE_MARKOV': MarkovPost,
    'POST_TYPE_D2V': Doc2VecSimilarityPost,
    'POST_TYPE_GIPHY': GifPost,
    'POST_TYPE_INTERACTIVE': InteractivePost
}


class PostManager(object):
    def __init__(self):
        self._max_history = 20
        self.posts = []
        self.posts.append(StartPost("POST_TYPE_START"))

    def _limit(self):
        """
        limits the list of posts
        """
        if len(self.posts) > self._max_history:
            self.posts.pop(0)

    def last(self):
        """
        :return: the last added post
        """
        return self.posts[-1]

    def add(self, postType):
        """
        adds a new post
        :param postType: type of the new post
        """
        new = self.get(postType, self.last())
        self.posts.append(new)
        self._limit()

    def add_random(self):
        """
        adds a new random post
        """
        random_type = random.choice(list(post_types.keys()))
        post = self.create_post(random_type, self.last())
        self.posts.append(post)
        self._limit()
        return post

    @staticmethod
    def create_post(post_type, previous):
        """
        returns a new Post() instance
        :param post_type: type of the new post
        :param previous: the previously generated post
        :return: a new post of certain type
        """
        return post_types[post_type](previous, post_type)
