import textblob
import random

if __name__ == '__main__':
    while True:
        input = raw_input('word: ')
        start_word = textblob.Word(input)
        print(start_word.spellcheck())
        if len(start_word.synsets) == 0:
            continue
        print('synsets: ' + str(start_word.synsets))
        print('definitions: ' + str(start_word.definitions))
        random_index = random.randint(0, len(start_word.synsets) -1)
        synonyme = start_word.synsets[random_index].name().partition('.')[0]
        synonyme = synonyme.replace('_', ' ')
        print(synonyme)
        synset_index = 0
        synset = start_word.synsets[synset_index]
        print('lemma_names' + str(synset.lemma_names))
        print('hypernyms: ' + str(synset.hypernyms()))
        print('hyponyms: ' + str(synset.hyponyms()))
        print('holonyms: ' + str(synset.member_holonyms()))
        print('meronyms: ' + str(synset.part_meronyms()))

