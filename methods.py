import cv2
import random
import colorsys
import numpy as np
from config import cfg
import json, random



def get_percentage(a, b):
    """Method use to get percentage given [a,b]"""
    return a / b * 100


def read_class_names(class_file_name):
    """Method to read class name:
       [ripe_pineapple, unripe_pineapple,
       ripe_papaya, unripe_papaya]"""
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names


def count_objects(data, by_class=False):
    """Method to count total object found or per class"""
    boxes, scores, classes, num_objects = data
    allowed_classes = list(read_class_names(cfg.YOLO.CLASSES).values())

    # create dictionary to hold count of objects
    counts = dict()

    # if by_class = True then count objects per class
    if by_class:
        class_names = read_class_names(cfg.YOLO.CLASSES)

        # loop through total number of objects found
        for i in range(num_objects):
            # grab class index and convert into corresponding class name
            class_index = int(classes[i])
            class_name = class_names[class_index]
            if class_name in allowed_classes:
                counts[class_name] = counts.get(class_name, 0) + 1
            else:
                continue



    # else count total objects found
    else:
        counts['total object'] = num_objects

    return counts


def get_parameters(data):
    """Method to return all parameters for a shelf data:
    Total fruit found, cant fruit per class in percentage,
    fruit type """
    all_object = count_objects(data, by_class=False)
    all_object_cant = all_object.get('total object')
    specific_object = count_objects(data, by_class=True)

    ripe_pineapple_predict = specific_object.get("ripe_pineapple")
    unripe_pineapple_predict = specific_object.get("unripe_pineapple")
    ripe_papaya_predict = specific_object.get("ripe_papaya")
    unripe_papaya_predict = specific_object.get("unripe_papaya")

    counted_classes = count_objects(data, by_class=True)

    percentage_ripe = 0.0
    percentage_unripe = 0.0

    cant_unripe = 0
    cant_ripe = 0

    fruit_type = ""

    for unripe_key_pineappe, unripe_value_pineapple in counted_classes.items():
        if unripe_key_pineappe == "unripe_pineapple":
            cant_unripe = unripe_value_pineapple
            fruit_type = "pineapple"

    for ripe_key_pineapple, ripe_value_ripe in counted_classes.items():
        if ripe_key_pineapple == "ripe_pineapple":
            cant_ripe = ripe_value_ripe
            fruit_type = "pineapple"

    for unripe_key_papaya, unripe_value_papaya in counted_classes.items():
        if unripe_key_papaya == "unripe_papaya":
            cant_unripe = unripe_value_papaya
            fruit_type = "papaya"

    for ripe_key_papaya, ripe_value_papaya in counted_classes.items():
        if ripe_key_papaya == "ripe_papaya":
            cant_ripe = ripe_value_papaya
            fruit_type = "papaya"

    if all_object_cant != 0:
        #recognition_data =  {"fruit_cant": all_object_cant, "fruit_type": fruit_type, "Ripe cant": cant_ripe, "Unripe cant": cant_unripe}
        #json_recognition_data = json.dumps(recognition_data, indent=4, default=str)
        return all_object_cant, fruit_type, cant_ripe, cant_unripe

    else:
        return 0,0,0,0

def format_boxes(bboxes, image_height, image_width):
    """Helper method to convert bounding boxes from normalized
       ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax"""
    for box in bboxes:
        ymin = int(box[0] * image_height)
        xmin = int(box[1] * image_width)
        ymax = int(box[2] * image_height)
        xmax = int(box[3] * image_width)
        box[0], box[1], box[2], box[3] = xmin, ymin, xmax, ymax
    return bboxes


def draw_bbox(image, bboxes, counted_classes=None, show_label=True):
    """Method to draw detections"""
    classes = read_class_names(cfg.YOLO.CLASSES)
    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    out_boxes, out_scores, out_classes, num_boxes = bboxes
    for i in range(num_boxes):
        if int(out_classes[i]) < 0 or int(out_classes[i]) > num_classes: continue
        coor = out_boxes[i]
        fontScale = 0.5
        score = out_scores[i]
        class_ind = int(out_classes[i])
        class_name = classes[class_ind]

        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

        if show_label:
            bbox_mess = '%s: %.2f' % (class_name, score)
            t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
            c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
            cv2.rectangle(image, c1, (np.float32(c3[0]), np.float32(c3[1])), bbox_color, -1)  # filled

            cv2.putText(image, bbox_mess, (c1[0], np.float32(c1[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)

        if counted_classes is not None:
            height_ratio = int(image_h / 25)
            offset = 15
            for key, value in counted_classes.items():
                cv2.putText(image, "{}s detected: {}".format(key, value), (5, offset),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
                offset += height_ratio
    return image
