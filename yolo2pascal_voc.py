import glob
import os
import shutil
from xml.dom.minidom import parseString

import numpy as np

import cv2
from lxml.etree import Element, SubElement, tostring


class Yolo2Pascal:
    def __init__(self, classes):
        self.classes = classes

    def get_images_paths(self, path):
        images_list = glob.glob(path + '/*.jpg')
        return images_list

    def convert_coords(self, class_id, width, height, x, y, w, h):
        xmax = int((x*width) + (w * width)/2.0)
        xmin = int((x*width) - (w * width)/2.0)
        ymax = int((y*height) + (h * height)/2.0)
        ymin = int((y*height) - (h * height)/2.0)
        class_id = int(class_id)
        return (class_id, xmin, xmax, ymin, ymax)

    def convert(self, path):
        print('[INFO]: start processing:' + path)
        pascal_path = path.split('/')[-1] + '_pascal'
        if not os.path.exists(pascal_path):
            os.makedirs(pascal_path)
        images_paths = self.get_images_paths(path=path)
        for image_path in images_paths:
            shutil.copy2(image_path, pascal_path + '/')
            annotation_path = os.path.splitext(image_path)[0] + '.txt'
            img = cv2.imread(image_path)
            base_image_path = image_path.split('/')[-1]

            height, width, channels = img.shape
            node_root = Element('annotation')
            node_folder = SubElement(node_root, 'folder')
            node_folder.text = 'VOC2007'

            node_filename = SubElement(node_root, 'filename')
            node_filename.text = base_image_path

            node_filename = SubElement(node_root, 'path')
            node_filename.text = os.path.join(pascal_path, base_image_path)

            node_source = SubElement(node_root, 'source')
            node_database = SubElement(node_source, 'database')
            node_database.text = 'Unknown'

            node_size = SubElement(node_root, 'size')
            node_width = SubElement(node_size, 'width')
            node_width.text = str(width)

            node_height = SubElement(node_size, 'height')
            node_height.text = str(height)

            node_depth = SubElement(node_size, 'depth')
            node_depth.text = str(channels)

            node_segmented = SubElement(node_root, 'segmented')
            node_segmented.text = '0'
            if os.path.exists(annotation_path):
                label_norm = np.loadtxt(annotation_path).reshape(-1, 5)

                for i in range(len(label_norm)):
                    labels_conv = label_norm[i]
                    new_label = self.convert_coords(
                        labels_conv[0], width, height, labels_conv[1],
                        labels_conv[2], labels_conv[3], labels_conv[4])
                    node_object = SubElement(node_root, 'object')
                    node_name = SubElement(node_object, 'name')
                    node_name.text = self.classes[new_label[0]]

                    node_pose = SubElement(node_object, 'pose')
                    node_pose.text = 'Unspecified'

                    node_truncated = SubElement(node_object, 'truncated')
                    node_truncated.text = '0'
                    node_difficult = SubElement(node_object, 'difficult')
                    node_difficult.text = '0'
                    node_difficult = SubElement(node_object, 'occluded')
                    node_difficult.text = '0'
                    node_bndbox = SubElement(node_object, 'bndbox')
                    node_xmin = SubElement(node_bndbox, 'xmin')
                    node_xmin.text = str(new_label[1])
                    node_ymin = SubElement(node_bndbox, 'ymin')
                    node_ymin.text = str(new_label[3])
                    node_xmax = SubElement(node_bndbox, 'xmax')
                    node_xmax.text = str(new_label[2])
                    node_ymax = SubElement(node_bndbox, 'ymax')
                    node_ymax.text = str(new_label[4])
                    xml = tostring(node_root, pretty_print=True)
                    dom = parseString(xml)
            xml_file = os.path.splitext(base_image_path)[0] + '.xml'
            f = open(os.path.join(pascal_path, xml_file), "wb")
            f.write(xml)
            f.close()
