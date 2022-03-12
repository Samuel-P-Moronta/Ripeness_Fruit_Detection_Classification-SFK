import socket
import json
import queue
import threading
from object_detection_classification import get_fruit_recognition


HEADER = 64
PORT = 6000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def ml_send():
    # return params
    q_cant = queue.Queue()
    q_type = queue.Queue()
    q_cant_ripe = queue.Queue()
    q_cant_unripe = queue.Queue()
    q_cant_overripe = queue.Queue()
    t1 = threading.Thread(target=get_fruit_recognition, name=get_fruit_recognition,
                          args=(q_cant, q_type, q_cant_ripe, q_cant_unripe, q_cant_overripe))
    t1.start()
    print("Getting info from image recognition")
    while True:
        value_cant = q_cant.get()
        value_type = q_type.get()
        value_cant_ripe = q_cant_ripe.get()
        value_cant_unripe = q_cant_unripe.get()
        value_cant_overripe = q_cant_overripe.get()

        reg_data = {"fruitCant": value_cant,
                    "fruitType": value_type,
                    "cantOverripe": value_cant_overripe,
                    "cantRipe": value_cant_ripe,
                    "cantUnripe": value_cant_unripe}

        json_reg_data = json.dumps(reg_data, indent=4, default=str)
        print(json_reg_data)
        message = json_reg_data.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        print("[SENDING] Sending message to ML server...")
        client.send(message)


if __name__ == '__main__':
    print("[STARTING] client ML is starting...")
    ml_send()
