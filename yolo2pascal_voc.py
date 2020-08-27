import os

import cv2
from pascal_voc_io import PascalVocWriter
from yolo_io import YoloReader


class Yolo2Pascal:
    def __init__(self, classes):
        self.classes = classes

    def convert(self, path):
        print('[INFO]: start processing:' + path)
        pascal_path = path.split('/')[-1] + '_pascal'
        if not os.path.exists(pascal_path):
            os.makedirs(pascal_path)
        images_paths = self.get_images_paths(path=path)
        for image_path in images_paths:
            annotation_path = image_path.split('.')[0] + '.txt'
            img = cv2.imread(image_path)
            image_shape = img.shape
            base_path = path.split('/')[-1]
            base_image_path = image_path.split('/')[-1]
            writer = PascalVocWriter(base_path, base_image_path,
                                     image_shape, localImgPath=image_path)

            # Read YOLO file

            tYoloParseReader = YoloReader(annotation_path, img)
            shapes = tYoloParseReader.getShapes()
            num_of_box = len(shapes)

            for i in range(num_of_box):
                label = shapes[i][0]
                xmin = shapes[i][1][0][0]
                ymin = shapes[i][1][0][1]
                x_max = shapes[i][1][2][0]
                y_max = shapes[i][1][2][1]

                writer.addBndBox(xmin, ymin, x_max, y_max, label, 0)

            writer.save(targetFile=pascal_path + '/' +
                        annotation_path.split('.')[0] + ".xml")
