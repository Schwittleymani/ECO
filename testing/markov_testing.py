# https://github.com/wieden-kennedy/python-markov
import markov

filename = 'boris_magrini-confronting_the_machine.txt'
file = open(filename, 'r')

boris_markov = markov.Markov(prefix=filename)
for s in file:
    boris_markov.add_line_to_index(s.split())

print(' '.join(boris_markov.generate(seed='can they'.split(), max_words=500)))

for i in range(10):
    answer = ' '.join(boris_markov.generate(max_words=500))
    score = boris_markov.score_for_line(answer.split())
    if score > 50:
        print(answer)
        print(score)
