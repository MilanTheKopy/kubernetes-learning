import os
import time
import socket
import random
import string
import threading

from http.server import HTTPServer, BaseHTTPRequestHandler


AGENT_NAME = os.getenv("AGENT_NAME", "unknown-agent") #hier lesen wir umgebungsvariablen aus. diese werden 
TARGET_HOST = os.getenv("TARGET_HOST") #im deployment unter containers/env definiert, siehe alpha deployment
PORT = 50000


def generate_message():
    random_part = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )
    return f"{AGENT_NAME}: {random_part}"


def tcp_server():
    with socket.create_server(("", PORT)) as s:
        s.listen()

        print(f"{AGENT_NAME}: server listening on port {PORT}", flush=True)

        while True:
            conn, addr = s.accept()

            with conn:
                data = conn.recv(1024)

                if not data:
                    continue

                message = data.decode()

                print(
                    f"{AGENT_NAME} received from {addr[0]}: {message}",
                    flush=True
                )

                response = f"ACK from {AGENT_NAME}"
                conn.sendall(response.encode())

def tcp_client():
    # kurz warten, bis Kubernetes und der andere Agent bereit sind
    time.sleep(5)
    print(f"AGENT_NAME: {AGENT_NAME}, TARGET_HOST: {TARGET_HOST}")
    while True:
        try:
            message = generate_message()

            with socket.create_connection((TARGET_HOST, PORT), timeout=5) as s:
                print(
                    f"{AGENT_NAME} -> {TARGET_HOST}: {message}",
                    flush=True
                )

                s.sendall(message.encode())

                response = s.recv(1024).decode()

                print(
                    f"{AGENT_NAME} received response: {response}",
                    flush=True
                )

        except Exception as e:
            print(
                f"{AGENT_NAME}: connection failed: {e}",
                flush=True
            )

        time.sleep(5)


def http_server():

    with HTTPServer(("", PORT)) as s:
        s


threading.Thread(target=tcp_server, daemon=True).start()

tcp_client()