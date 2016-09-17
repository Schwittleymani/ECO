import grammar_check
import sys


def correct(text,recursive = True):
	tool = grammar_check.LanguageTool('en-GB')
	matches = tool.check(text)
	while len(matches) > 0:
		print 'grammar correct: ',len(matches)
		for co in matches:
			print co
		text = grammar_check.correct(text, matches)
		matches = tool.check(text)
	return text


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "ERROR: just one string as parameter, bitch"
	else:
		print correct(sys.argv[1])
