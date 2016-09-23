import enchant.checker
import grammar_check


class PreProcessor(object):
    def __init__(self):
        self.chkr = enchant.checker.SpellChecker("en_US")
        self.MAX_GRAMMAR_RECURSION = 20

    def process(self, text):
        """
        run spell check first, then grammar check on the output of that

        :param text:
        :return:
        """
        spell_checked = self.spell_check(text)
        grammar_checked = self.grammar_check(text)
        combined = self.grammar_check(spell_checked)
        return combined, spell_checked, grammar_checked

    def grammar_check(self, text, recursive = True):
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
            print 'grammar correct: ', len(matches)
            for co in matches:
                print co
            text = grammar_check.correct(text, matches)
            recs += 1
            if not recursive or recs > self.MAX_GRAMMAR_RECURSION:
                break
            matches = tool.check(text)
        return text

    def spell_check(self, text):
        self.chkr.set_text(text)
        for err in self.chkr:
            print("ERROR:", err.word)
            suggestions = self.chkr.suggest(err.word)
            if self.chkr.suggest(len(err.word) > 0):
                err.replace(suggestions[0])
        return self.chkr.get_text()
