import enchant.checker
import grammar_check
import textblob
import random
import unicodedata


class PreProcessor(object):
    def __init__(self):
        self.chkr = enchant.checker.SpellChecker("en_US")
        self.MAX_GRAMMAR_RECURSION = 20

    def process(self, text, return_to_lower=True):
        """
        run spell check first, then grammar check on the output of that

        :param text:
        :return:
        """

        print('Processing input: ' + text)

        unicode_input = unicode(text.decode('ascii', 'ignore'))
        ascii_input = unicodedata.normalize('NFKD', unicode_input).encode('ascii', 'ignore')

        # double spell checks
        spell_checked = self.__spell_check(ascii_input)
        spell_checked = self.__correct_via_synonyme(spell_checked)
        #spell_checked = self.__spell_check_textblob(spell_checked)
        grammar_checked = self.__grammar_check(ascii_input)
        combined = self.__grammar_check(spell_checked)

        if return_to_lower:
            return combined.lower(), spell_checked.lower(), grammar_checked.lower()
        else:
            return combined, spell_checked, grammar_checked

    def __grammar_check(self, text, recursive=True):
        """
        recursiveness can't be deactivated from outside atm

        :param text:
        :param recursive:
        :return:
        """
        tool = grammar_check.LanguageTool('en-GB')
        try:
            matches = tool.check(text)
        except:
            return text
        recs = 0
        while len(matches) > 0:
            #print 'grammar correct: ', len(matches)
            for co in matches:
                pass
                #print co
            text = grammar_check.correct(text, matches)
            recs += 1
            if not recursive or recs > self.MAX_GRAMMAR_RECURSION:
                break
            matches = tool.check(text)
        return text

    def __spell_check(self, text):
        try:
            self.chkr.set_text(text)
            for err in self.chkr:
                #print("ERROR:", err.word)
                suggestions = self.chkr.suggest(err.word)
                if self.chkr.suggest(len(err.word) > 0):
                    err.replace(suggestions[0])
            return self.chkr.get_text()
        except IndexError:
            print('Spellchecker ERROR')
            return text

    def __correct_via_synonyme(self, text):
        start_word = textblob.Word(text)
        if len(start_word.synsets) == 0:
            return text
        print('synsets: ' + str(start_word.synsets))
        print('definitions: ' + str(start_word.definitions))
        random_index = random.randint(0, len(start_word.synsets) - 1)
        synonyme = start_word.synsets[random_index].name().partition('.')[0]
        synonyme = synonyme.replace('_', ' ')
        return synonyme

    def __spell_check_textblob(self, text):
        """
        could be that this is the same implementation that is used in the
        enchant spell checker. the implementation of this one is taken from
        here http://norvig.com/spell-correct.html
        :param text:
        :return:
        """
        words = text.split()
        finished = []
        for word in words:
            w = textblob.Word(word)
            # always using the word with the highest confidence
            # in case its complete bullshit, the bullshit word is at index 0
            corrected = w.spellcheck()[0][0]
            finished.append(corrected)

        return ' '.join(finished)