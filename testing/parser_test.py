import textparser

import pyPdf

text1 = ""

pdf = pyPdf.PdfFileReader(open('boris-magrini_confronting_the_machine.pdf', "rb"))
for page in pdf.pages:
    text1 += page.extractText()

print('Parsing text from pyPDF')
parser1 = textparser.TextParser()
parser1.parse(text1)

out1 = open('out1.txt', 'w')
for s in parser1.proper_sentences:
    out1.write(s.string.encode('utf8'))
    out1.write('\n')
out1.close()

############################


file = open('boris_magrini-confronting_the_machine.txt', 'r')
text2 = file.read()
text2 = unicode(text2, "utf-8")

print('Parsing text from pdftotext')
parser2 = textparser.TextParser()
parser2.parse(text2)

out2 = open('out2.txt', 'w')
for s in parser2.proper_sentences:
    out2.write(s.string.encode('utf8'))
    out2.write('\n')
out2.close()

############################
# Tika is bad, dont use it

#import tika
#tika.initVM()
#from tika import parser

#text3 = parser.from_file('boris-magrini_confronting_the_machine.pdf')["content"]
#parser3 = textparser.TextParser()

#print('Parsing text from Tika')
#parser3.parse(text3)

#out3 = open('out3.txt', 'w')
#for s in parser3.proper_sentences:
#    out3.write(s.string.encode('utf8'))
#    out3.write('\n')
#out3.close()

############################

import textract

text4 = textract.process('boris-magrini_confronting_the_machine.pdf')
parser4 = textparser.TextParser()

print('Parsing text from texttract')
parser4.parse(text4)

out4 = open('boris_magrini-confronting_the_machine.txt', 'w')
for s in parser4.proper_sentences:
    out4.write(s.string.encode('utf8'))
    out4.write('\n')
out4.close()