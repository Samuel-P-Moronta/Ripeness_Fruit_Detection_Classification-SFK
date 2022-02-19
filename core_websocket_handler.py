import socket
import websocket
import _thread
from datetime import datetime, time
import time
import json, random
import queue
import threading
from threading import Thread
import traceback

from object_detection_classification import get_fruit_recognition
import ML_socket_server as ML


# ++++++++++++++++++++++++++++++++++++++
#                                      #
# SMART FOOD KEEPER-FINAL PROJECT BY:  #
# SAMUEL P. MORONTA | YEHUDY DE PEÑA   #
#                                      #
# ++++++++++++++++++++++++++++++++++++++#


HEADER = 64
PORT = 6000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def generate_container_data():
    """
    This functions is to receive data from load cell
    and adjust the values to send it to the server
    in java with the endpoint [server/container]
    """
    maxWeight = 5
    # Insert function to get weight data here
    ###################################################
    weight_data_in = round(random.uniform(0.00, 5.00), 2)

    weight = 0
    status_code = 0
    # To keep correct values
    if weight_data_in > 0:
        weight = weight_data_in

        if weight <= maxWeight / 3:
            # Minimun level in container
            status_code = 1
        elif weight > maxWeight / 3 and weight <= (maxWeight / 3) * 2:
            # Middle level in container
            status_code = 2
        else:
            # Full level in container
            status_code = 3
    elif weight_data_in == 0:
        status_code = 1

    else:
        # wrong data received
        return "Calibrar el sensor"

    # To send sensor data as JSON format
    container_data = {'weight': weight, 'statusCode': status_code}

    json_sensor_data = json.dumps(container_data, indent=4, default=str)

    return json_sensor_data


def handle_client(conn, addr,que_msg):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            que_msg.put(msg)

    conn.close()

def send_sensor_data(ws):
    def run(*args):
        i = 0
        random.seed(datetime.now())
        temperature = round(random.uniform(30.00, 31.00), 2)
        humidity = round(random.uniform(60.00, 61.00), 2)

        server.listen()
        q_msg = queue.Queue()
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, q_msg))
        thread.start()
        try:
            while True:
                print("[GETTING] Getting info from ML client")
                msg = q_msg.get()
                json_object = json.loads(msg)

                print(json_object)
                print("Sending msg to backend")

                q_cant = json_object["fruitCant"]
                q_fruitType = json_object["fruitType"]
                q_cant_overripe = json_object["cantOverripe"]
                q_cant_ripe = json_object["cantRipe"]
                q_cantUnripe = json_object["cantUnripe"]

                reg_data = {"temperature":temperature,
                            "humidity":humidity,
                            "fruitCant": q_cant,
                            "fruitType": q_fruitType,
                            "cantOverripe": q_cant_overripe,
                            "cantRipe": q_cant_ripe,
                            "cantUnripe": q_cantUnripe}

                json_reg_data = json.dumps(reg_data, indent=4, default=str)

                ws.send(json_reg_data)
                print("+++++++++++++++++++++++++++++++++++")
                i = i + 1
            ws.close()
            print("thread terminating...")

        except Exception:
            print(traceback.format_exc())

    _thread.start_new_thread(run, ())


def send_container_data(ws):
    def run(*args):
        i = 0
        while True:
            print("[*] Sending data # [{}] to container ".format(i))
            data = generate_container_data()
            time.sleep(10)
            # websocket.
            ws.send(data)
            print("+++++++++++++++++++++++++++++++++++")
            i = i + 1
        # time.sleep(1)
        ws.close()
        print("thread terminating...")

    _thread.start_new_thread(run, ())


def connect_websocket_shelf():
    """
    Function to connect websocket shelf endponit /server/shelf
    """
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:7000/server/shelf",on_open=send_sensor_data,on_message=on_message,on_error=on_error,on_close=on_close)
    ws.run_forever()


def connect_websocket_container():
    """
    Function to connect websocket container endponit /server/container
    """
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:7000/server/container", on_open=send_container_data,on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    "Threading to keep twice function running"
    Thread(target=connect_websocket_container).start()
    Thread(target=connect_websocket_shelf).start()
