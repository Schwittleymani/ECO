import gensim
import spacy
import codecs


from src.python.doc2vecbuilder import basepath_folder
# from src.python.doc2vecbuilder.basepath_folder import Basepath

FORMAT_DOC_PER_LINE = 0
FORMAT_DOC_PER_FILE = 1

# brought it over to nlp
class CorpusModel:

    def __init__(self, basepath, data_format):
        self.base_corpus_dir = basepath_folder.Basepath(basepath_folder.host_specific_base_data_dir(basepath))
        self.base_model_dir = basepath_folder.host_specific_model_file(basepath)

        # print(self.base_corpus_dir.base_path)
        # dump(self.base_corpus_dir.doc_count_tree())

        self.data_format = data_format

        # print (self.base_corpus_dir)
        # print(self.base_model_dir)
        # self.sentences = []
        # self.model_file = model_file
        # self.model = None
        # if os.path.isdir(doc_file_folder):
        #     self.doc_folder = []

        # bp = basepath_folder.Basepath('')

    def load_sentences(self):
        sentences = []
        for doc in self.doc_folder:
            for uid, line in enumerate(open(doc)):
                ls = gensim.models.doc2vec.TaggedDocument(words=line.split(), tags=['SENT_%s' % uid])
                sentences.append(ls)
        # print
        len(sentences), 'sentences'

    def train(self):
        model = gensim.models.Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
        print('building vocab')
        model.build_vocab(self.sentences)

        base_alpha = model.alpha
        base_min_alpha = model.min_alpha

        # for mepoch in range(2):
        #     model.alpha = base_alpha
        #     model.min_alpha = base_min_alpha
        for epoch in range(10):
            print('epoch',  10 + epoch)
            model.train(self.sentences)
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay
            # shuffle(sentences)

        # saving the model
        model.save(self.model_file)
        print ('model trained and saved')

    def load_model(self):
        self.model = gensim.models.Doc2Vec.load(self.model_file)
        'model loaded.', len(self.model.docvecs), 'vectors'

    def compare_lengths(self):
        if len(self.sentences) != len(self.model.docvecs):
            print
            'something is fishy, unequal length: ', len(self.sentences), 'sentences and', len(self.model.docvecs), 'vectors'

    def spacy_tokenize(self, doc_id):
        if self.data_format == FORMAT_DOC_PER_FILE:
            # docs = self.base_corpus_dir.get_files('', True)
            # doc = docs[doc_id]
            txt = self.load_doc(doc_id)
            en_nlp = spacy.load('en')
            doc = en_nlp(txt)
            # print(txt)
            print(doc[0])
        else:
            pass
            # TODO load from sentences.

    def load_doc(self, doc_id, from_filtered=True):
        if self.data_format == FORMAT_DOC_PER_FILE:
            doc = self.base_corpus_dir.get_files('', True, from_filtered)[doc_id]
            return read(doc)
        else:
            pass
            # TODO load from sentences.


def read(doc_path):
    with codecs.open(doc_path, encoding='utf-8') as input:
        return input.read()

import os
def cool_file(path_):
    # print('checking '+ path_)
    return path_.endswith('_valid.txt') and os.stat(path_).st_size > 0

if __name__ == "__main__":
    cm = CorpusModel('NAIL_DATAFIELD_txt/parsed_v3/library_and_archive_theory', FORMAT_DOC_PER_FILE)
    # cm.spacy_tokenize(0)
    # base_folder = doc2vec_helper.base_txt_folder('NAIL_DATAFIELD_txt/parsed_v3/')
    # print(len(cm.base_corpus_dir.get_files('', True)))
    files = cm.base_corpus_dir.get_files()
    print(len(files))
    # files = [f for f in files if cool_file(f)]
    # print(files)
    # print(len(files))
    # files