import markovify

with open("boris_magrini-confronting_the_machine.txt", "r", encoding="utf-8") as txt:
    text = txt.read()

print(text)
text_model = markovify.Text(text)


print(text_model.make_sentence_with_start('to the'))