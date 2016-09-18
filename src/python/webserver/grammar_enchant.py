import enchant
import enchant.checker
from enchant.checker.CmdLineChecker import CmdLineChecker

chkr = enchant.checker.SpellChecker("en_US")
chkr.set_text("this is sme example txt")
for err in chkr:
    print "ERROR:", err.word
    suggestions = chkr.suggest(err.word)
    if chkr.suggest(len(err.word) > 0):
        err.replace(suggestions[0])

print chkr.get_text()