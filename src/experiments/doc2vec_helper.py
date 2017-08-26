import os, socket

# from doc2vec.settings import L

def init_logs():
    if not os.path.exists('logs'):
        os.makedirs('logs')

def model_basedir():        # host_specific_
    return host_specific_model_file('')

# def host_specific_basedir(dir):
#     host = socket.gethostname()
#     if host == 'lyrik':
#         print('U ARE ON LYRIK')
#         return LYRIK_BASE_DATAFOLDER+dir
#         # ... move data and model into some convinient folder. so that model/parsed_v3_valid is there and
#         # NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt is there
#     else:
#         # local
#         # TODO WRONG: data folder
#         return '../../models/'

def host_specific_model_file(file_name):        
    host = socket.gethostname() 
    if host == 'lyrik':
        print('U ARE ON LYRIK')
        return '/home/ramin/projects/ECO/src/python/modelbuilder/'+file_name
        # ... move data and model into some convinient folder. so that model/parsed_v3_valid is there and
        # NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt is there
    else:
        # local
        return '../../models/'+file_name

def base_txt_folder(path = ''):
    # TODO add the stable-path code here  
    return txt_file(path + '')
    
def txt_file(file_name):
    host = socket.gethostname() 
    if host == 'lyrik':
        return '/home/marcel/drive/data/eco/'+file_name
    else:
        # local
            return '../../data/'+file_name # parsed_v3_all.txt

    # TODO: catch non existence and throw message!
    # if not os.path.isfile(model_file):
    #     print "TEXTFILE FILE IS NOT THERE"
    

# base_dir = '../../data/parsed_v3/'
# base_dir += 'arts_arthistory_aesthetics'




# base_folder = base_txt_folder('NAIL_DATAFIELD_txt/parsed_v3/')
# # print(os.listdir(base_folder))
#
# path = BasePath(base_folder)
# path.get_dirs('')

# path.doc_count_tree()


