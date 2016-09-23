import enchant.checker
import grammar_check

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
        unicode_input = unicode(text.decode('ascii', 'ignore'))
        ascii_input = unicodedata.normalize('NFKD', unicode_input).encode('ascii', 'ignore')

        spell_checked = self.__spell_check(ascii_input)
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
        matches = tool.check(text)
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
        self.chkr.set_text(text)
        for err in self.chkr:
            #print("ERROR:", err.word)
            suggestions = self.chkr.suggest(err.word)
            if self.chkr.suggest(len(err.word) > 0):
                err.replace(suggestions[0])
        return self.chkr.get_text()
