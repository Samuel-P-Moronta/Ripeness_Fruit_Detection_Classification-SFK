import socket
import threading
import queue
HEADER = 64
PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

"Socket connection with ML client"


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

"""
def start():
    server.listen()
    q_msg = queue.Queue()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr, q_msg))
    thread.start()
    while True:
        print("Getting info from ML client")
        msg = q_msg.get()
        print(msg)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
"""
