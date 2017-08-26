import os
import socket
from src.python.doc2vecbuilder.settings import LYRIK_BASE_DATA_DIR,LYRIK_BASE_MODEL_DIR,LOCAL_BASE_DATA_DIR,LOCAL_BASE_MODEL_DIR


class Basepath:

    def __init__(self, base_path):
        self.base_path = base_path
        if not self.base_path.endswith('/'):
            self.base_path += '/'

    def path(self, file_name):
        return self.base_path + file_name

    def get_dirs(self, sub=''):
        return [f for f in os.listdir(self.base_path + sub) if os.path.isdir(self.path(sub + f))]

    def get_files(self, sub='', complete_path=False, filtered=True):
        files = [f for f in os.listdir(self.base_path + sub) if os.path.isfile(self.path(sub + f))]

        if filtered:
            files = self.my_filter(files)
        if complete_path:
            files = [self.path(f) for f in files]
        return files

    def my_filter(self, file_paths):
        def cool_file(path_):
            # print('checking '+ path_)
            return path_.endswith('_valid.txt') and os.stat(path_).st_size > 0
        return [f for f in file_paths if cool_file(self.path(f))]

    def doc_count_tree(self, complete = False):
        def count_sub_dirs(directory=''):
            subs = self.get_dirs(directory)
            sub_dict = {sub: count_sub_dirs(directory + sub + '/') for sub in subs}
            if len(sub_dict) > 0:
                sum_subs = sum([value['total_files'] for key, value in sub_dict.items()])
                sum_subs_filtered = sum([value['total_filtered'] for key, value in sub_dict.items()])
            else:
                sum_subs = 0
                sum_subs_filtered = 0
            files = self.get_files(directory)
            dir_files = len(files)
            filtered_files = len(self.my_filter([directory + fi for fi in files]))
            total_files = sum_subs + dir_files
            total_filtered = sum_subs_filtered + filtered_files
            ret = {"files": dir_files,
                   'filtered_files': filtered_files,
                   'total_files': total_files,
                   'total_filtered': total_filtered,
                   }
            if len(sub_dict) > 0 and complete:
                ret['sub'] = sub_dict
                ret['sum_subs'] = sum_subs
                ret['sum_subs_filtered'] = sum_subs_filtered
            return ret
        return count_sub_dirs('')


def init_logs():
    if not os.path.exists('logs'):
        os.makedirs('logs')


def model_basedir():  # host_specific_
    return host_specific_model_file('')


def host_specific_base_data_dir(directory):
    host = socket.gethostname()
    if host == 'lyrik':
        print('U ARE ON LYRIK')
        directory = LYRIK_BASE_DATA_DIR + directory
        # ... move data and model into some convinient folder. so that model/parsed_v3_valid is there and
        # NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt is there
    else:
        # local
        # TODO WRONG: data folder
        directory = LOCAL_BASE_DATA_DIR + directory
    if not os.path.exists(directory):
        print('the data directory does not exist')
    return directory


def host_specific_model_file(directory):
    host = socket.gethostname()
    if host == 'lyrik':
        print('U ARE ON LYRIK')
        directory = LYRIK_BASE_MODEL_DIR + directory
    else:
        # local
        directory = LOCAL_BASE_MODEL_DIR + directory
    if not os.path.exists(directory):
        print('the model directory does not exist')
    return directory


def base_txt_folder(path=''):
    # TODO add the stable-path code here
    return txt_file(path + '')


def txt_file(file_name):
    host = socket.gethostname()
    if host == 'lyrik':
        return '/home/marcel/drive/data/eco/' + file_name
    else:
        # local
        return '../../data/' + file_name  # parsed_v3_all.txt