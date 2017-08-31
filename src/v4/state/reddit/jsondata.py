import os
import sys
import json
import logging
import datetime
import time
import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

NUM_PARTS = 100

log = logging.getLogger(__name__)

# loader that is set up to load data in the
# format that spark exports it

# iterator of json rows of data, when data is saved out of
# spark engine
class SparkJsonSource(object):
    def __init__(self, json_source, block_words=[], validation_fn=None):
        self.feather_file = json_source
        self.block_words = block_words
        self.validation_fn = validation_fn

    def is_valid(self, row):
        if self.validation_fn:
            return self.validation_fn(row)
        else:
            return True

    def exists(self, json_source=None):
        base_dir = self.base_dir if json_source is None \
            else os.path.join('.', json_source)
        return os.path.exists(base_dir)

    def has_block_words(self, sen):
        if len(self.block_words) == 0:
            return False
        for word in self.block_words:
            if word in sen.lower():
                return True
        return False

    def __iter__(self):
        print("reading from " + self.feather_file)

        # loop here
        onlydirs = [f for f in listdir(self.feather_file) if isdir(join(self.feather_file, f))]
        print(str(onlydirs))
        for dir in onlydirs:
            path_to_folder = join(self.feather_file, dir)
            print(path_to_folder)
            path = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]
            print(str(path))

            #json_files = [pos_json for pos_json in os.listdir(path_to_folder) if pos_json.endswith('.json')]

            count = 0
            file_counter = 0
            #progress = unbounded_progress_bar("Reading:")
            for index, js in enumerate(path):
                with open(os.path.join(path_to_folder, js)) as json_file:
                    for line in json_file:
                        row = json.loads(line)
                        #days = MAX_DAYS_HISTORY if MAX_DAYS_HISTORY != 0 else 99999
                        #t = datetime.date.today() - datetime.timedelta(days=days)
                        #unix_time_yesterday = int(t.strftime("%s"))
                        #unix_time_downloaded = int(row['downloaded_utc'])
                        #if unix_time_downloaded < unix_time_yesterday:
                            # skipping if the comment is older than MAX_AGE_DAYS
                        #    continue
                        sen = row['s'] if 's' in row else row['r_body']
                        if self.has_block_words(sen):
                            continue
                        if not self.is_valid(row):
                            log.debug("Not valid, skipping: '{0}' ".format(row['s']))
                            continue
                        yield row
                        count += 1
                        #if count % 10000 == 0:
                        #    progress.update(count)
                file_counter += 1

# iterator of rows of data, when data has been saved in simple json
# format compatible with Ryan's code
class RyanFormatJsonSource():

    def __init__(self, json_file_path):
        if not os.path.exists(json_file_path):
            raise ValueError("Could not find file " + json_file_path)
        self.json_file_path = json_file_path

    def __iter__(self):

        with open(self.json_file_path) as simple_json_data:
            # FIXME there's actually just one line normally
            # cant figure out 'readToEnd()' without wifi
            for line in simple_json_data:
                data = json.loads(line)
                for row in data["lines"]:
                    yield row


class JsonData(object):
    def __init__(self, json_source, block_words=[]):
        self.block_words = block_words
        self._data = None
        self.json_source = json_source

    def load(self):
        spark_src = SparkJsonSource(self.json_source, block_words=self.block_words)
        self._data = []
        count = 0
        for row in iter(spark_src):
            self._data.append(row)
            count += 1
        log.debug(" loaded (%i rows)" % len(self._data))

    def save(self, data, json_target=None):
        base_dir = self.base_dir if json_target is None \
                   else os.path.join('.', json_target)

        # ensure directory
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        parts = self.into_parts(data, NUM_PARTS)
        i = -1
        for part in parts:
            i += 1
            file_path = os.path.join(base_dir, "data_{num:05d}.json".format(num=i))
            with open(file_path, mode="w", encoding="utf8") as outfile:
                for row in part:
                    outfile.write(json.dumps(row))
                    outfile.write("\n")
            #progress(float(i) / NUM_PARTS, msg="saving..")
        #progress(1, msg="saving..")

    @staticmethod
    def into_parts(l, num_parts):
        n = len(l) / num_parts
        n = max(1000, int(n))
        return (l[i:i + n] for i in range(0, len(l), n))

    def exists(self, json_source=None):
        base_dir = self.base_dir if json_source is None \
            else os.path.join('.', json_source)
        return os.path.exists(base_dir)

    def ensure_data(self):
        if not self._data:
            self.load()
        return self._data

    def __iter__(self):
        self.ensure_data()
        self.iter_pos = 0
        return self

    # iterating though pre-loaded, in memory data
    def __next__(self):
        if self.iter_pos>=len(self._data):
            raise StopIteration
        self.iter_pos += 1
        return self._data[self.iter_pos-1]

    def sort(self, sort_key_fn):
        self.ensure_data()
        self._data.sort(key=sort_key_fn)

    @property
    def data(self):
        self.ensure_data()
        return self._data
