
from os import listdir
from os.path import isdir
from os.path import join


def get_directories_from_path(path):
    return [directory for directory in listdir(path) if isdir(join(path, directory))]

