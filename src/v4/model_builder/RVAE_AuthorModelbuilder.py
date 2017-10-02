from src.v4.pytorch_RVAE import train_word_embeddings, train 
import shutil
import os
import codecs
from random import random
import codecs
import json


def read_json_file(file_name):
    with codecs.open(file_name,encoding='utf-8') as fin:
        return json.loads(fin.read())

def merge_docs(author_name,log_file, dest_folder = None,overwrite= False):
    log = read_json_file(log_file)
    author_docs = [doc for doc in list(log['file_descriptors'].values()) if doc['author_name'] == author_name]

    base_folder = get_data_folder() + log["folder_path"] 
    print(base_folder)
    if not os.path.isdir(base_folder):
        print('''Value: "%s" is not set correctly. Cannot find folder:\n%s
        The folder is relative to the project data folder\nBYE''' %("folder_path", base_folder))
        return
    if not dest_folder:
        dest_folder = base_folder + "merged/"
    dest_file = (dest_folder + author_name + '.txt').replace(",","_")
    
    print("Creating:",dest_file)
    
    if not os.path.exists(dest_folder): os.makedirs(dest_folder)
        
    if os.path.isfile(dest_file) and not overwrite:
        print('File %s exists already & overwrite is not set. ending here...' %(dest_file))
        return dest_file
    
    def get_docs_abs_path(doc_dict):
        return base_folder + doc_dict["rel_path"] + doc_dict["file_name"]
    
    file_names = [get_docs_abs_path(doc) for doc in author_docs]
    print('Merging %s files' % len(file_names))
    return dest_file

    
    with codecs.open(dest_file, 'w') as outf:
        for fname in file_names:
            if not os.path.exists(fname):
                print("%s\ndoes not exist. skipping")
                continue
            with open(fname) as inf:
                for line in inf:
                    outf.write(line)
                    
    print("DONE!\nResulting file is a size of %s bytes" % os.stat(dest_file).st_size)

def split_for_train_test(file_path, destination_folder = None, test_ratio = 0.05, overwrite=False):
        if not destination_folder:
            destination_folder = file_path[:file_path.rindex('.')]+'_SPLIT/'
        print("Splitting %s" % file_path)
        print("Destination folder:",destination_folder)
        
        if not os.path.exists(destination_folder): os.makedirs(destination_folder)
            
        fout_train = destination_folder + 'train.txt'
        fout_test = destination_folder + 'test.txt'
        
        if os.path.exists(fout_train) and not overwrite:
            print("%s exists and overwrite is not set.\nBye" % fout_train)
            return

        if os.path.exists(fout_test) and not overwrite:
            print("%s exists and overwrite is not set. Bye" % fout_test)
            return
            
            
        f_in = codecs.open(file_path, 'r', 'UTF-8')
        f_out_train = codecs.open(fout_train, 'w', 'UTF-8')
        f_out_test = codecs.open(fout_test, 'w', 'UTF-8')

        for line in f_in:
            if random() < test_ratio:
                f_out_test.write(line)
            else:
                f_out_train.write(line)
        print("DONE")


def author_folder_name(author_name):
    return author_name.replace(",","_")

def prepare_rvae_train(author_name,log_file,rvae_data_folder):
    merged_file = merge_docs(author_name,log_file)
    split_for_train_test(merged_file,rvae_data_folder,overwrite=True)

def run_rvae():
    train_word_embeddings.run()
    train.run()
    pass

def move_rvae_model_files(rvae_data_folder, model_folder):
    model_files = os.listdir(rvae_data_folder)
    for file in model_files:
        shutil.move(rvae_data_folder + file,model_folder + file)
    
log_file = 'log-final.json'
rvae_data_folder = get_project_folder() + 'src/v4/pytorch_RVAE/data/'
author_model_folder = get_data_folder() + author_folder_name('Chomsky,Noam') + '/'
        
prepare_rvae_train('Chomsky,Noam',log_file, rvae_data_folder)
run_rvae()
move_rvae_model_files(rvae_data_folder,)        
