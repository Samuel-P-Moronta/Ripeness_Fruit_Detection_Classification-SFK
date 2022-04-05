from object_detection_classification import get_fruit_recognition
import queue
import numpy as np
import _thread
from datetime import datetime, time
import json, random
import queue
import threading
import itertools



if __name__ == '__main__':
    # return params
    cant = get_fruit_recognition()
    for i in cant:
        print("Getting info from image recognition")
        value_cant = next(get_fruit_recognition())
        value_type = next(get_fruit_recognition())
        value_cant_ripe = next(get_fruit_recognition())
        value_cant_unripe = next(get_fruit_recognition())
        value_cant_overripe = next(get_fruit_recognition())
        print(value_cant,value_type,value_cant_ripe,value_cant_unripe,value_cant_overripe)