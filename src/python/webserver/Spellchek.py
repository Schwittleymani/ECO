import enchant.checker

chkr = enchant.checker.SpellChecker("en_US")

def spell_check(text):
    chkr.set_text(text)
    for err in chkr:
        print "ERROR:", err.word
        suggestions = chkr.suggest(err.word)
        if chkr.suggest(len(err.word) > 0):
            err.replace(suggestions[0])
    return chkr.get_text()

