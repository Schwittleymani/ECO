from markov import Markov

filename = 'boris_magrini-confronting_the_machine.txt'
file = open(filename, 'r')

boris_markov = Markov(prefix=filename)
for s in file:
    boris_markov.add_line_to_index(s.split())

print(' '.join(boris_markov.generate(seed='can they'.split(), max_words=100)))

for i in xrange(10):
    answer = ' '.join(boris_markov.generate(max_words=100))

    print(answer)
    print(boris_markov.score_for_line(answer.split()))
