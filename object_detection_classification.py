import json
import os
import time
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
import methods
import socket
import json

HEADER = 64
PORT = 6000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def get_fruit_recognition():

    IOU_THRESHOLD = 0.45
    MAX_OUTOUT_SIZE_PER_CLASS = 50
    MAX_TOTAL_SIZE = 50
    SCORE_THRESHOLD = 0.60
    MODEL_FILE_NAME = r'C:\Users\SMORONTA\Desktop\Ripeness_Fruit_Detection_Classification-SFK\checkpoints\yolov4-416'

    # begin video capture
    try:
        vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #vid = cv2.VideoCapture("http:/192.168.1.131:7070/?action=stream/0")
    except ValueError:
        print("Error")

    saved_model_loaded = tf.saved_model.load(MODEL_FILE_NAME, tags=[tag_constants.SERVING])
    infer = saved_model_loaded.signatures['serving_default']

    frame_num = 0
    # Loop for applying object detection

    while True:

        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_num += 1
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break

        image_data = cv2.resize(frame, (416, 416))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()


        # Load pre-trained weights and apply object detection
        batch_data = tf.constant(image_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=MAX_OUTOUT_SIZE_PER_CLASS,
            max_total_size=MAX_TOTAL_SIZE,
            iou_threshold=IOU_THRESHOLD,
            score_threshold=SCORE_THRESHOLD
        )

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = frame.shape
        bboxes = methods.format_boxes(boxes.numpy()[0], original_h, original_w)

        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

        # count objects found
        counted_classes = methods.count_objects(pred_bbox, by_class=True)
        params = methods.get_parameters(pred_bbox)
        all_object_cant, fruit_type, cant_ripe,cant_unripe,cant_overripe = params

        #return params
        #list_elements_recognition = [all_object_cant,fruit_type,cant_ripe,cant_unripe,cant_overripe]

        #yield list_elements_recognition

        reg_data = {"fruitCant": all_object_cant,
                    "fruitType": fruit_type,
                    "cantOverripe": cant_ripe,
                    "cantRipe": cant_unripe,
                    "cantUnripe": cant_overripe}

        json_reg_data = json.dumps(reg_data, indent=4, default=str)
        print(json_reg_data)
        message = json_reg_data.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        print("[SENDING] Sending message to ML server...")
        client.send(message)

        """
        q_cant.put(all_object_cant)
        q_type.put(fruit_type)
        q_cant_ripe.put(cant_ripe)
        q_cant_unripe.put(cant_unripe)
        q_cant_overripe.put(cant_overripe)
        """

        fps = 1.0 / (time.time() - start_time)
        #print("FPS: %.2f" % fps)
        image = methods.draw_bbox(frame, pred_bbox, counted_classes)

        np.asarray(image)
        cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imshow("result", result)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("[STARTING] client ML is starting...")
    get_fruit_recognition()