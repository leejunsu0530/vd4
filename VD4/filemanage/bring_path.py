import sys
import os


def bring_file_path():
    path = os.path.abspath(sys.argv[0])
    return path


def bring_file_name():
    path = bring_file_path()
    file = os.path.basename(path)  # / 스플릿해서 가장 마지막
    return file


def bring_file_name_no_ext():
    file = bring_file_name()
    file_lst = os.path.splitext(file)
    return file_lst[0]


if __name__ == '__main__':
    print(bring_file_path())
    print(bring_file_name())
    print(bring_file_name_no_ext())
