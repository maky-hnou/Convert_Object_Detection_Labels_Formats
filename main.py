import re
import sys

from pascal_voc2yolo import Pascal2Yolo
from yolo2pascal_voc import Yolo2Pascal

if __name__ == '__main__':
    classes = input('[INFO]: Please type the categories of '
                    'the dataset separated by a coma (,)\n'
                    'categories: ')
    classes = re.sub(r' ', '', classes)
    classes = classes.split(',')
    action = input('[INFO]: Please choose an action\n'
                   '1: convert Pascal to YOLO\n'
                   '2: convert YOLO to Pascal\n'
                   'action: ')
    data_paths = input('[INFO]: Please type the folders paths '
                       'separated by a coma (,)\n'
                       'folders: ')
    data_paths = re.sub(r' ', '', data_paths)
    data_paths = data_paths.split(',')
    if action == '1':
        pascal2yolo = Pascal2Yolo(classes=classes)
        for path in data_paths:
            pascal2yolo.convert(path=path)
    elif action == '2':
        yolo2pascal = Yolo2Pascal(classes=classes)
        for path in data_paths:
            yolo2pascal.convert(path=path)
    else:
        print('Wrong choice')
        sys.exit(0)
