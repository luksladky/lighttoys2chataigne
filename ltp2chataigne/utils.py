import math
import os
import shutil

def make_dir_if_not_exists(project_name):
    try:
        os.mkdir(f"../{project_name}/")
    except FileExistsError:
        print(f"Files in the folder \"{project_name}\" are going to be overwritten.")


def make_path_if_not_exists(path):
    os.makedirs(path, exist_ok=True)


def change_path_to_script_dir():
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)


def remove_dir(path):
    shutil.rmtree(path, ignore_errors=True)


def change_ext(filename, ext):
    parts = filename.split('.')
    parts[-1] = '.' + ext
    filename = "".join(parts)
    return filename

def chataigne_time(original_time: int) -> float:
    return float(original_time) / 1000.0


def decimal_part(x) -> float:
    int_part = int(math.floor(x))
    dec_part = int((x - int_part))
    return dec_part