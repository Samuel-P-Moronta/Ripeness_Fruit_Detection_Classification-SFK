from object_detection_classification import get_fruit_recognition
import queue
import websocket

import threading
import _thread
from datetime import datetime, time
import json, random
import queue
from threading import Thread

def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def send_sensor_data(ws):
    def run(*args):
        i = 0

        q_cant = queue.Queue()
        q_type = queue.Queue()
        q_cant_ripe = queue.Queue()
        q_cant_unripe = queue.Queue()
        q_cant_overripe = queue.Queue()
        t1 = threading.Thread(target=get_fruit_recognition, name=get_fruit_recognition,
                              args=(q_cant, q_type, q_cant_ripe, q_cant_unripe, q_cant_overripe))
        t1.start()

        while True:
            print("[*] Sending image recognition to websocket server[{}] ".format(i))
            fruitCant = q_cant.get()
            fruitType = q_type.get()
            cantRipe = q_cant_ripe.get()
            cantUnripe = q_cant_unripe.get()
            cantOverripe = q_cant_overripe.get()

            reg_data = {"fruitCant": fruitCant, "fruitType": fruitType, "cantOverripe": cantOverripe,
                        "cantRipe": cantRipe,
                        "cantUnripe": cantUnripe}

            json_reg_data = json.dumps(reg_data, indent=4, default=str)

            # time.sleep(10)
            ws.send(json_reg_data)
            print("+++++++++++++++++++++++++++++++++++")
            i = i + 1
        ws.close()
        print("thread terminating...")

    _thread.start_new_thread(run, ())

def connect_websocket_shelf():
    """
    Function to connect websocket shelf endponit /server/shelf
    """

    websocket.enableTrace(True)
    # Change localhost to your current ip localhost example: 10.0.0.10
    ws = websocket.WebSocketApp("ws://localhost:8000",
                                on_open=send_sensor_data,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    "Threading to keep twice function running"
    Thread(target=connect_websocket_shelf).start()
