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
    weight_data_in = round(random.uniform(0.00, 5.00), 2)
    container_data = {
        'container':1,
        'weight': weight_data_in
    }
    json_sensor_data = json.dumps(container_data, indent=4, default=str)

    return json_sensor_data

def send_sensor_data(ws):
    def run(*args):
        i = 0
        random.seed(datetime.now())
        temperature = round(random.uniform(30.00, 31.00), 2)
        humidity = round(random.uniform(60.00, 61.00), 2)
        server.listen()
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        try:
            while True:
                print("[GETTING] Getting info from ML client")

                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    # Recibo todas las informaciones del reconocimiento
                    msg = conn.recv(msg_length).decode(FORMAT)
                    json_object = json.loads(msg)
                    fruit_cant = json_object["fruitCant"]
                    fruit_type = json_object["fruitType"]
                    cant_overripe = json_object["cantOverripe"]
                    cant_ripe = json_object["cantRipe"]
                    cant_unripe = json_object["cantUnripe"]
                    deviceId = "1"

                    reg_data = {
                        "deviceId": deviceId,
                        "temperature": temperature,
                        "humidity": humidity,
                        "fruitCant": fruit_cant,
                        "fruitType": fruit_type,
                        "cantOverripe": cant_overripe,
                        "cantRipe": cant_ripe,
                        "cantUnripe": cant_unripe
                    }
                    json_reg_data = json.dumps(reg_data, indent=4, default=str)
                    ws.send(json_reg_data)

            conn.close()
            ws.close()
            print("thread terminating...")

        except Exception:
            print(traceback.format_exc())

    _thread.start_new_thread(run, ())


def simulate_realtime_ml_data_1(ws):
    def run(*args):
        while True:
            temperature = round(random.uniform(25.00, 38.00), 2)
            humidity = round(random.uniform(50.00, 60.00), 2)
            overripe = 3
            ripe = 1
            unripe = 1
            fruitCant = 4

            random_reg_data = {
                "deviceId": "2",
                "temperature": temperature,
                "humidity": humidity,
                "fruitCant": fruitCant,
                "fruitType": "papaya",
                "cantOverripe": overripe,
                "cantRipe": ripe,
                "cantUnripe": unripe
            }
            json_reg_data = json.dumps(random_reg_data, indent=4, default=str)
            time.sleep(20)
            ws.send(json_reg_data)
        ws.close()
    _thread.start_new_thread(run, ())


def simulate_realtime_ml_data_2(ws):
    def run(*args):
        while True:
            temperature = round(random.uniform(25.00, 38.00), 2)
            humidity = round(random.uniform(50.00, 60.00), 2)
            overripe = 0
            ripe = 2
            unripe = 1
            fruitCant = 3

            random_reg_data = {
                "deviceId": "3",
                "temperature": temperature,
                "humidity": humidity,
                "fruitCant": fruitCant,
                "fruitType": "pineapple",
                "cantOverripe": overripe,
                "cantRipe": ripe,
                "cantUnripe": unripe
            }
            json_reg_data = json.dumps(random_reg_data, indent=4, default=str)
            time.sleep(10)
            ws.send(json_reg_data)
        ws.close()
    _thread.start_new_thread(run, ())


def simulate_realtime_ml_data_3(ws):
    def run(*args):
        while True:
            temperature = round(random.uniform(30.00, 40.00), 2)
            humidity = round(random.uniform(55.00, 70.00), 2)
            overripe = 1
            ripe = 2
            unripe = 2
            fruitCant = 4

            random_reg_data = {
                "deviceId": "4",
                "temperature": temperature,
                "humidity": humidity,
                "fruitCant": fruitCant,
                "fruitType": "papaya",
                "cantOverripe": overripe,
                "cantRipe": ripe,
                "cantUnripe": unripe
            }
            json_reg_data = json.dumps(random_reg_data, indent=4, default=str)
            time.sleep(10)
            ws.send(json_reg_data)
        ws.close()
    _thread.start_new_thread(run, ())


def send_container_data(ws):
    def run(*args):
        i = 0
        while True:
            print("DIGITE UN PESO: ")
            x = input();
            container_data = {
                'containerId': "1",
                'weight': x
            }
            json_sensor_data = json.dumps(container_data, indent=4, default=str)
            ws.send(json_sensor_data)
        """
        while True:
            print("[*] Sending data # [{}] to container ".format(i))

            weight_data_in = round(random.uniform(0, 5), 1)
            container_data = {
                'containerId': "1",
                'weight': weight_data_in
            }
            json_sensor_data = json.dumps(container_data, indent=4, default=str)
            time.sleep(10)
            ws.send(json_sensor_data)
            print("+++++++++++++++++++++++++++++++++++")
            i = i + 1
        # time.sleep(1)
        ws.close()
        """
        print("thread terminating...")

    _thread.start_new_thread(run, ())


def connect_websocket_shelf():
    """
    Function to connect websocket shelf endponit /server/shelf
    """
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:7000/server/shelf", on_open=send_sensor_data, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever()


def connect_websocket_shelf_simulate_1():
    """
    Function to connect websocket shelf endponit /server/shelf
    """
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:7000/server/shelf", on_open=simulate_realtime_ml_data_1, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.run_forever()

def connect_websocket_container():
    """
    Function to connect websocket container endponit /server/container
    """
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:7000/server/container", on_open=send_container_data,
                                on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    "Threading to keep twice function running"
    #Thread(target=connect_websocket_container).start()
    Thread(target=connect_websocket_shelf).start()
    #Thread(target=connect_websocket_shelf_simulate_1).start()