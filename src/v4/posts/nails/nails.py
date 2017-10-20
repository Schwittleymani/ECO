import time
import numpy as np
import feather
import operator
import gensim
from nltk.corpus import stopwords
from misc import data_access


class NailsSimilarityFinder(object):
    def __init__(self, w2v_model):
        self._model = w2v_model

        feather_path = 'pandas/parsed_v3_log-final_arts_arthistory_aesthetics_bigger_than_2.feather'
        print('Loading ' + feather_path)
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
            words = "interactive installation electronic chaos oracle chat program creative partner database writing".split()
            for word in words:
                v = self._model[word]
                vectors.append(v)

        if len(vectors) == 0:
            print('if this error occurs, we should initialize the vectors list with one random 300dim vector...')

        vector = np.mean(vectors, axis=0)
        return vector

    def calc_closest_index(self, df, target_vector):
        vectors = {}
        for i in range(len(df)):
            sen = df.iloc[i]['sentence']
            vec = self.to_vector(sen)
            vectors[i] = vec

        distances = {}
        for index, vector in vectors.items():
            d = np.linalg.norm(vector-target_vector)
            distances[index] = d

        sorted_distances = sorted(distances.items(), key=operator.itemgetter(1))
        return int(sorted_distances[0][0])

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

        index = self.calc_closest_index(ldf, sentence_vec)
        author = ldf.iloc[index]['author']
        sentence = ldf.iloc[index]['sentence']
        #source = ldf.iloc[index]['source']
        options = num_selection
        return author, sentence, options

if __name__ == "__main__":
    w2v_path = 'word2vec_models/wiki_plus_v3_valid_combined.txt_numpy.w2vmodel'
    print('Loading w2v model: ' + w2v_path)
    model = gensim.models.Word2Vec.load(data_access.get_model_folder() + w2v_path)
    finder = NailsSimilarityFinder(model)
    start_time = time.time()
    author, sentence, options = finder.get_similar('Geeks and freaks become what they are negatively , through the exclusion by others , but together form a class .')
    print('author: ' + author)
    print('sentence: ' + sentence)
    #print('source: ' + source)
    print('options: ' + str(options))
    end_time = time.time() - start_time
    print(str(end_time) + ' seconds.')