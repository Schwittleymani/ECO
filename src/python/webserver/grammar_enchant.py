import enchant
import enchant.checker
from enchant.checker.CmdLineChecker import CmdLineChecker

chkr = enchant.checker.SpellChecker("en_US","this is sme example txt")
for err in chkr:
    print "ERROR:", err.word
#cmdln = CmdLineChecker()
#cmdln.set_checker(chkr)
#cmdln.run()
print chkr.get_text()