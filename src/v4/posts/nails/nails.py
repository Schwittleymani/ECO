import random
import time
import numpy as np
import feather
from nltk.corpus import stopwords
from misc import data_access


class NailsSimilarityFinder(object):
    def __init__(self, w2v_model):
        self._model = w2v_model

        feather_path = 'parsed_v3_log-final_arts_arthistory_aesthetics_bigger_than_2.feather'
        self._dataframe = feather.read_dataframe(data_access.get_model_folder() + feather_path)

    # sentence to vector via w2v
    def to_vector(self, sentence):
        sentence = sentence.lower()
        # not using english stop words, only using content words
        words = [word for word in sentence.split() if (word not in stopwords.words("english") and word in self._model.vocab)]

        vectors = []
        for word in words:
            v = self._model[word]
            vectors.append(v)

        if len(vectors) == 0:
            print('if this error occurs, we should initialize the vectors list with one random 300dim vector...')

        vector = np.mean(vectors, axis=0)
        #print(model.similar_by_vector(vector))
        return vector

    def get_similar(self, sentence):
        ldf = self._dataframe
        sentence_vec = self.to_vector(sentence)

        num_selection = 0
        dist = 0.05
        for i in range(300):
            tdf = ldf[(ldf['p'+str(i)] > sentence_vec[i]-dist) & (ldf['p'+str(i)] < sentence_vec[i]+dist)]
            num_sentences = len(tdf.index)
            if num_sentences > 0:
                ldf = tdf
                num_selection = num_sentences
            if num_sentences < 5:
                print('stopped at index ' + str(i))
                break

        index = random.randint(0, len(ldf) - 1)
        return ldf.iloc[index], num_selection

if __name__ == "__main__":
    finder = NailsSimilarityFinder()
    start_time = time.time()
    selection = finder.get_similar('Geeks and freaks become what they are negatively , through the exclusion by others , but together form a class .')
    print('author: ' + selection['author'])
    print('sentence: ' + selection['sentence'])
    print('source: ' + selection['filename'])
    end_time = time.time() - start_time
    print(str(end_time) + ' seconds.' )