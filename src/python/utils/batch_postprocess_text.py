import os
import sys

source_folder = '/mnt/drive1/data/eco/pdf_to_text/'
dest_folder = '/mnt/drive1/data/eco/pdf_to_text_postprocessed/'

if len(sys.argv) > 1:
    source_folder = sys.argv[1] + "/"

if len(sys.argv) > 2:
    dest_folder = sys.argv[2] + "/"

if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

for file in os.listdir(source_folder):
    print file
    print source_folder + file
    cmd = "pdftotext " + source_folder + file + " " + dest_folder + file[:-3] + "txt"
    cmd = 'python /home/marcel/projects/eco/src/python/utils/text_postprocessor.py --input ' + source_folder + file + ' --output ' + dest_folder + file
    print cmd
    os.system(cmd)
