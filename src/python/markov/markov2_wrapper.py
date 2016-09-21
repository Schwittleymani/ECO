from markov2 import Markov

file = open('gene_youngblood-expanded_cinema.txt')

markov = Markov(file)

input = 'there is nothing to do'.split()

text = markov.generate_markov_text(input, 50)

del input[-1]
del input[-1]

output = ' '.join(input)
output += ' ' + text
print(output)