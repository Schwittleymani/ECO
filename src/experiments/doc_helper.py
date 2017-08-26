import codecs

def make_doc_one_liner(doc_file):
    """
    turns a document with one sentence per line into a document with all sentences in one line
    returns the path of the new file
    """
    with codecs.open(doc_file, 'r', 'UTF-8') as file_int:
        new_file_path = add_file_descriptor(doc_file,'1Line')
        with codecs.open(new_file_path, 'w', 'UTF-8') as file_out:
            for l in file_int:
                file_out.write(l.strip() +' ')
    return new_file_path

def add_file_descriptor(file_name, descriptor):
    """
    add a file descriptor which attached to the end of the file name with _<descriptor>
    use for something like _valid, _fault, _1Line
    """
    ending = file_name[file_name.rfind('.'):]
    return file_name[:file_name.rfind('.')] + '_' + descriptor + ending


def read_text(doc_file):
    """
    utf-8 read whole document
    """
    with codecs.open(doc_file, 'r', 'UTF-8') as file_int:
        return file_int.read()