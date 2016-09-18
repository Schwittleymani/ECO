import grammar_check
import sys

max_recs = 20

def correct(text,recursive = True):
	"""
	recursiveness can't be deactivated from outside atm
	"""
	tool = grammar_check.LanguageTool('en-GB')
	matches = tool.check(text)
	recs = 0
	while len(matches) > 0:
		print 'grammar correct: ',len(matches)
		for co in matches:
			print co
		text = grammar_check.correct(text, matches)
		recs += 1
		if not recursive or recs > max_recs:
			break
		matches = tool.check(text)
	return text


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "ERROR: just one string as parameter, bitch"
	else:
		print correct(sys.argv[1])


