from gensim.models.doc2vec import Doc2Vec
import textacy
from misc import data_access
import random
from functools import reduce

def sentence_to_clean_word_list(text, get_named_entities=False):
    s_doc = textacy.Doc(text, lang='en').spacy_doc
    for t in s_doc:
        clean_words = [t.lemma_ for t in s_doc if not (t.is_punct or t.is_stop or t.lemma_ == '' or t.is_space)]
    if not get_named_entities:
        return clean_words, []
    else:
        return clean_words, [entity.text for entity in s_doc.ents]


def get_similar(model, words, top_n):
    inferred_vector = model.infer_vector(words)
    sims = model.docvecs.most_similar([inferred_vector], topn=top_n)
    return sims


class Doc2VecSimilarities:

    def __init__(self, model_file_path, text_file_path):
        print("Loading model: " + model_file_path)
        self.model = Doc2Vec.load(model_file_path)
        print("Reading corpus")
        self.text = list(textacy.fileio.read.read_file_lines(text_file_path))

    def get_top_n(self,
                  sentence,
                  top_n=10,
                  trash_scores=True,
                  only_indices=False,
                  min_score=0):
        words = sentence_to_clean_word_list(sentence)[0]
        results = get_similar(self.model, words, top_n)
        return_list = []
        try:
            for result in results:
                if result[1] > min_score:
                    sentence = int(result[0]) if only_indices else self.text[result[0]].strip()
                    res = sentence if trash_scores else (sentence, result[1])
                    return_list.append(res)
        except IndexError as err:
            print(err)
            print(results)
            return [self.select_random()]
        return return_list

    def get_all_more_similar_then(self,
                                  sentence,
                                  min_score=0.8,
                                  max_results=10,
                                  trash_scores=True,
                                  only_indices=False):
        return self.get_top_n(sentence, max_results, trash_scores, only_indices, min_score)

    def select_random(self):
        print("RANDOM")
        return random.choice(self.text)

    def sort_emotional_valence(self,sentence):
        resp = self.get_top_n(sentence,15)
        count_valence = []
        for re in resp:
            se = textacy.doc.Doc(re, lang='en')
            valence = textacy.lexicon_methods.emotional_valence(se)
            pos_vals = [valence[v] for v in valence if v in ['INSPIRED', 'HAPPY', 'AMUSED']]
            pos = reduce((lambda pos, val: pos + val), pos_vals)
            neg_vals = [valence[v] for v in valence if v in ['ANGRY', 'AFRAID', 'SAD']]
            neg = reduce((lambda neg, val: neg + val), neg_vals)
            count_valence.append((re, pos, neg))


        sorted_valence = sorted(count_valence, key=lambda rank_sen: rank_sen[1] - rank_sen[2], reverse=True)
        return [sentence_val[0] for sentence_val in sorted_valence]



corpus_file_path = data_access.get_data_folder() + 'fortune/fortune-gen.txt'
model_file_path = data_access.get_model_folder() + "doc2vec/fortune-gen.doc2vec"

model = None

def load_model():
    global model
    model = Doc2VecSimilarities(model_file_path, corpus_file_path)

