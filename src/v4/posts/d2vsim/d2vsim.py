from misc import data_access
import os
from gensim.models.doc2vec import Doc2Vec,TaggedDocument
import textacy
from tqdm import tqdm, trange
import json


base_folder = data_access.get_data_folder() + 'NAIL_DATAFIELD_txt/parsed_v3/merged/'

def name_to_file_name(author_name, file_format='txt'):
    return (author_name + '.' + file_format).replace(",", "_")


def get_author_file(author_name):
    return base_folder + name_to_file_name(author_name)


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


def author_model_path(author_name):
    return data_access.get_model_folder() + "doc2vec/" + name_to_file_name(author_name, 'doc2vec')


def save_model(model, mode_file_path):
    model.clear_sims()
    model.delete_temporary_training_data()
    model.save(mode_file_path)


def load_author_model(author_name):
    return Doc2Vec.load(author_model_path(author_name))


class StreamTaggedDocumentobject:
    def __init__(self, file_path, store_while_streaming=True, named_entity_tags=False):
        self.file_path = file_path
        self.store_while_streaming = store_while_streaming
        self.temp_tagged_docs_file_path = self.file_path + '.taggeddocs.json'
        self.named_entity_tags = named_entity_tags

    def __iter__(self):
        if self.store_while_streaming:
            temp_file = open(self.temp_tagged_docs_file_path, 'w')
        for uid, line in enumerate(open(self.file_path)):
            words, entities = sentence_to_clean_word_list(line, self.named_entity_tags)
            tags = [uid]
            if self.named_entity_tags:
                tags += entities
            tagged_doc = TaggedDocument(words=words, tags=tags)
            if self.store_while_streaming:
                temp_file.write(json.dumps({"words": tagged_doc.words, "tags": tagged_doc.tags}) + '\n')
            yield tagged_doc


class StreamTaggedDocumentFile:
    def __init__(self, tagged_doc_file_path):
        self.file_path = tagged_doc_file_path

    def __iter__(self):
        with open(self.file_path) as fin:
            for line in fin:
                td = json.loads(line)
                yield TaggedDocument(words=td["words"], tags=td["tags"])


class Doc2VecSimilarities:
    def __init__(self, model_file_path, text_file_path):
        print("Loading model")
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
        for result in results:
            if result[1] > min_score:
                sentence = int(result[0]) if only_indices else self.text[result[0]].strip()
                res = sentence if trash_scores else (sentence, result[1])
                return_list.append(res)
        return return_list

    def get_all_more_similar_then(self,
                                  sentence,
                                  min_score=0.8,
                                  max_results=10,
                                  trash_scores=True,
                                  only_indices=False):
        return self.get_top_n(sentence, max_results, trash_scores, only_indices, min_score)

    def get_wmdistance(self):
        return self.model.wv.wmdistance('germany, europe, politics', 'england war, terror, drons')


class AuthorDoc2VecSimilarities(Doc2VecSimilarities):
    def __init__(self, author_name):
        Doc2VecSimilarities.__init__(self, author_model_path(author_name), get_author_file(author_name))


def create_model(corpus_file_path, model_file_path):
    model = Doc2Vec(size=100, min_count=2, iter=55)
    tagged_docs_stream = StreamTaggedDocumentobject(corpus_file_path)
    print("building model from", corpus_file_path)
    print("building vocab...")
    model.build_vocab(tagged_docs_stream)
    tagged_docs_stream = StreamTaggedDocumentFile(tagged_docs_stream.temp_tagged_docs_file_path)
    print("training model...")
    model.train(tagged_docs_stream, total_examples=model.corpus_count, epochs=model.iter)
    print(model.estimate_memory())
    print("saving model to", model_file_path)
    save_model(model, model_file_path)
    print('done')


def create_author_model(author_name):
    create_model(get_author_file(author_name), author_model_path(author_name))

if __name__ == "__main__":
    #create_author_model("Chomsky,Noam")
    #create_author_model("Ascott,Roy")
    #create_author_model("Dean,Jodi")
    #create_author_model("Featherstone,Mike")
    #create_author_model("Goldman,Emma")
    #create_author_model("Hayles,Katherine")
    #create_author_model("Lovink,Geert")
    #create_author_model("Thacker,Eugene")
    #create_author_model("Turkle,Sherry")

    sims = []
    #sims.append(AuthorDoc2VecSimilarities("Chomsky,Noam"))
    #sims.append(AuthorDoc2VecSimilarities("Ascott,Roy"))
    #sims.append(AuthorDoc2VecSimilarities("Dean,Jodi"))
    #sims.append(AuthorDoc2VecSimilarities("Featherstone,Mike"))
    #sims.append(AuthorDoc2VecSimilarities("Goldman,Emma"))
    #sims.append(AuthorDoc2VecSimilarities("Hayles,Katherine"))
    #sims.append(AuthorDoc2VecSimilarities("Lovink,Geert"))
    #sims.append(AuthorDoc2VecSimilarities("Thacker,Eugene"))
    #sims.append(AuthorDoc2VecSimilarities("Turkle,Sherry"))

    #print(json.dumps(sim.get_top_n("West germany is the shit. literally it is shit", 10), indent=2))
    #print(json.dumps(sim.get_all_more_similar_then("fact is freedom in Nicaragua is a fraud .", 0.55, trash_scores=False), indent=2))