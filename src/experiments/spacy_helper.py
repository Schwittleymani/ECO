
import spacy
import doc_helper

nlp = spacy.load('en')
    
class Spacy_helper:
    
    def __init__(self):
        pass
        
    def doc_clean_tokenz(self, doc_file):
        text = doc_helper.read_text(doc_file)
        doc = nlp(text)
        yield doc
        tokenz_clean = [token for token in doc if not token.is_stop]
        yield tokenz_clean
        
    def doc_yield_lemmas(self, tokenz):
        return (token.lemma_ for token in tokenz)