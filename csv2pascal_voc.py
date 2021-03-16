import os
import pandas as pd

from xml.dom.minidom import parseString
from lxml.etree import Element, SubElement, tostring


class Csv2Pascal():
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def get_classes(self):
        data = pd.read_csv('Meta.csv')
        classes = list(data['ClassId'])
        return classes

    def create_label(self):
        df = pd.read_csv(self.csv_file_path)
        for index, row in df.iterrows():
            width = row['Width']
            height = row['Height']
            x1 = row['Roi.X1']
            y1 = row['Roi.Y1']
            x2 = row['Roi.X2']
            y2 = row['Roi.Y2']
            category = row['ClassId']
            img_path = row['Path']

            node_root = Element('annotation')
            node_folder = SubElement(node_root, 'folder')
            node_folder.text = 'VOC2007'

            node_filename = SubElement(node_root, 'filename')
            node_filename.text = img_path

            node_filename = SubElement(node_root, 'path')
            node_filename.text = img_path

            node_source = SubElement(node_root, 'source')
            node_database = SubElement(node_source, 'database')
            node_database.text = 'Unknown'

            node_size = SubElement(node_root, 'size')
            node_width = SubElement(node_size, 'width')
            node_width.text = str(width)

            node_height = SubElement(node_size, 'height')
            node_height.text = str(height)

            node_depth = SubElement(node_size, 'depth')
            node_depth.text = str(3)

            node_segmented = SubElement(node_root, 'segmented')
            node_segmented.text = '0'

            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = str(category)

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
            node_xmin.text = str(x1)
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(y1)
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(x2)
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(y2)
            xml = tostring(node_root, pretty_print=True)
            parseString(xml)
            xml_file = os.path.splitext(img_path)[0] + '.xml'
            f = open(xml_file, "wb")
            f.write(xml)
            f.close()
