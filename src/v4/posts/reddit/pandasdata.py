import os
import sys
import json
import logging
import pandas as pd
import feather

from posts.reddit.jsondata import SparkJsonSource

NUM_PARTS = 100

log = logging.getLogger(__name__)


class PandasData(object):
    def __init__(self, feather_file,
                 block_words=[],
                 validation_fn=None,
                 numeric_cols=['s_len', 's_vbe', 's_count', 'post_pos', 's_shannon'],
                 reconstruct_posts=True,
                 force_read_from_json=False
                 ):
        self.path_to_feather = feather_file
        self.block_words = block_words
        self._df = None
        self.loaded_from_feather = False
        self.validation_fn = validation_fn
        self.reconstruct_posts_on_load = reconstruct_posts
        self.numeric_cols = numeric_cols
        self.force_read_from_json = force_read_from_json

    def load(self):
        if os.path.exists(self.path_to_feather) and not self.force_read_from_json:
            # load from dataframe saved as 'feather' format
            self._df = feather.read_dataframe(self.path_to_feather)
            self.loaded_from_feather = True
        else:
            # load from spark compatible 'json' format..

            spark_src = SparkJsonSource(self.path_to_feather, block_words=self.block_words, validation_fn=self.validation_fn)
            tmp = []
            for row in iter(spark_src):
                tmp.append(row)
            df = pd.DataFrame.from_dict(tmp)
            # convert numeric columns to numeric
            numeric_cols = self.numeric_cols
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

            self._df = df
            log.debug("loaded (%i sentences)" % len(self._df))

            # expand sentences to post length, where specified
            if self.reconstruct_posts_on_load:
                posts_df = self.reconstruct_posts()
                self._df = self._df.append(posts_df)

    def save(self, json_target):
        if not json_target.endswith(".feather"):
            json_target += ".feather"
        log.info('saving to ' + json_target)
        feather.write_dataframe(self._df, json_target)

    def ensure_feather_file_exists(self):
        self.ensure_data()
        if not self.loaded_from_feather:
            self.save()

    #def exists(self, json_source=None):
    #    base_dir = self.base_dir if json_source is None \
    #        else os.path.join(ROOT_DATA_DIR, json_source)
    #    return os.path.exists(base_dir)

    def sort(self, by):
        self.ensure_data()
        self._df.sort_values(by=by, axis=0, inplace=True)
        # it's assumed we're gonna want this sort to stick around/get used
        self._df.reset_index(drop=True)

    @staticmethod
    def get_path_to_feather(base_dir, json_source):
        path_to_feather = os.path.join(base_dir, json_source.replace(".json", ".feather"))
        if not path_to_feather.endswith(".feather"):
            path_to_feather += ".feather"
        return path_to_feather

    def reconstruct_posts(self, use_all_data=True):
        """reconstruct full posts for content marked with p_incl=True"""
        log.debug("reconstructing full posts..")
        df = self._df
        if not use_all_data:
            # only look at sentences marked with "p_incl" = post included
            candidates = df[(df.p_incl)]
        else:
            # assume all sentences have full post in current context
            candidates = df[(df.author != "4chan")]
        if len(candidates) == 0:
            return
        candidates.is_copy = False
        candidates.sort_values(['post_id', 'post_pos'], inplace=True)

        def aggregate_fn(x):

            # # its a shame to have to essentially re-do the
            # # schema here but im not sure how to avoid that
            return pd.Series({
                "w2v_avg_distance": x["w2v_avg_distance"].mean() if x["w2v_avg_distance"].min() > -1 else -1,
                "p_incl": False,
                "author": x["author"].min(),
                "s_vbe": x["s_vbe"].sum() / x["s_len"].sum(), # weighted average
                "post_pos": -1,
                "subreddit": x["subreddit"].min(),
                "w2v_total_distance": x["w2v_total_distance"].sum(),
                "post_id": x["post_id"].min(),
                "s": "%s" % ' '.join(x['s']),
                "unique_s_count": x["s_hash"].nunique(),
                "score": x["score"].min(),
                "s_count": 1, # an assumption, but seems reasonable
                "parent_id": x["parent_id"].min(),
                "s_len": x["s_len"].sum() + x["s"].count() -1, # accounting for spaces between
                "s_hash": None, # ideally we'd compute this again at this point
                "out_of_vocab_fraction": x["out_of_vocab_fraction"].mean(),
                "is_post": True
            })


        posts_df = candidates.groupby(['post_id']).apply(aggregate_fn)
        # it would be so much better to do the above step in parallel
        # unfortunately it has 'cant pickle' errors
        # posts_df = apply_parallel(candidates.groupby(['post_id']),aggregate_fn)

        # we need to eliminate cases where the same post is included twice (can happen due to resampling)
        # or where only one sentence is actually there but it is marked as p_incl (post included)
        posts_df = posts_df[posts_df.unique_s_count > 1]
        log.debug("reconstructed {0} full posts ".format(len(posts_df)))
        # for row in posts_df.itertuples(index=True, name='xyz'):
        #     print(row)
        return posts_df


    def ensure_data(self):
        if self._df is None or self._df.empty:
            self.load()

    @property
    def df(self):
        self.ensure_data()
        return self._df

    @property
    def second_longest_len(self):
        self.ensure_data()
        df = self._df
        return df.nlargest(2,'s_len').min().s_len

    @property
    def highest_sentence_count(self):
        self.ensure_data()
        df = self._df
        return df.nlargest(1,'s_count').min().s_count