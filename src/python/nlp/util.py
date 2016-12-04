import logging
import sys
import os
import pathlib

def get_last_dir_from_path(path):
    list = path.split('/')
    if path.endswith('/'):
        out = list[-2]
    else:
        out = list[-1]
    return out

def enable_verbose_training(program):
    program = os.path.basename(program)
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

def export_model(model, input_path, ext):
    # the input path is used for constructing the filename of the model
    model_filename = get_last_dir_from_path(input_path) + ext
    # file exists already in current directory?
    if pathlib.Path(model_filename).is_file():
        # y/n choice to overwrite
        user_input = input('Overwrite model file ' + model_filename + '? [y/(n)]')
        if 'y' in user_input:
            model.save(model_filename)
            print('Saved model: ' + model_filename)
        else:
            print('NOT saved model. File already exists.')
    else:
        model.save(model_filename)
        print('Saved model: ' + model_filename)