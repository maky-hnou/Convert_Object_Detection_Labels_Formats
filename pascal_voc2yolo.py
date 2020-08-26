import glob
import os
import shutil
import xml.etree.ElementTree as ET


class Pascal2Yolo:
    def __init__(self, classes):
        self.classes = classes

    def get_images_paths(self, path):
        images_list = glob.glob(path + '/*.jpg')
        return images_list

    def convert_coords(self, size, box):
        dw = 1./(size[0])
        dh = 1./(size[1])
        x = (box[0] + box[1])/2.0 - 1
        y = (box[2] + box[3])/2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x, y, w, h)

    def convert_annotation(self, dir_path, output_path, image_path):
        basename = os.path.basename(image_path)
        basename_no_ext = os.path.splitext(basename)[0]

        in_file = open(dir_path + '/' + basename_no_ext + '.xml')
        out_file = open(output_path + '/' + basename_no_ext + '.txt', 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in self.classes or int(difficult) == 1:
                continue
            cls_id = self.classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text),
                 float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = self.convert_coords((w, h), b)
            out_file.write(str(cls_id) + " " +
                           " ".join([str(a) for a in bb]) + '\n')

    def convert(self, path):
        print('[INFO]: start processing:' + path)
        yolo_path = path.split('/')[-1] + '_yolo'
        if not os.path.exists(yolo_path):
            os.makedirs(yolo_path)
        images_paths = self.get_images_paths(path=path)
        list_file = open(path.split('/')[-1] + '.txt', 'w')
        for image_path in images_paths:
            shutil.copy2(image_path, yolo_path + '/')
            list_file.write(image_path + '\n')
            self.convert_annotation(path, yolo_path, image_path)
        list_file.close()
        print('[INFO]: finished processing:' + path)
